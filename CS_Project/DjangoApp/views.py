import requests
from django.shortcuts import render
from .models import Author, Paper
from django.contrib.auth.decorators import login_required

def author_detail(request, author_id):
    author = Author.objects.get(AuthorID=author_id)
    authored_papers = author.authored_set.all()
    context = {
        'author': author,
        'authored_papers': authored_papers
    }
    return render(request, 'author_detail.html', context)

def paper_detail(request, paper_id):
    paper = Paper.objects.get(PaperID=paper_id)
    context = {
        'paper': paper
    }
    return render(request, 'paper_detail.html', context)

def login(request):
    return render(request, 'login.html')

@login_required
def doi_form(request):
    return render(request, 'doi_form.html')

@login_required
def main_form(request):
    if request.method == 'GET':
        doi_id = request.GET['doi']
        api_key = 'API_KEY'
        url = f'https://api.elsevier.com/content/abstract/doi/{doi_id}?apiKey={api_key}'
        print(url)
        response = requests.get(url, headers={'Accept': 'application/json'})
        if response.status_code == 200:
            data = response.json()["abstracts-retrieval-response"]
            print(data)
            # Extract relevant data from the response
            authors_data = data["coredata"]["dc:creator"]["author"]
            author_ids = ""
            author_names = ""
            for author in authors_data:
                if authors_data.index(author) == len(authors_data) - 1:
                    author_ids += author["@auid"]
                    author_names += author["preferred-name"]["ce:given-name"]
                else:
                    author_ids += author["@auid"] + ","
                    author_names += author["preferred-name"]["ce:given-name"] + ","
                    
            publisher_id = "Not Found"
            if "source-id" in data["coredata"]:
                publisher_id = data["coredata"]["source-id"]

            publisher_name = "Not Found"
            if "dc:publisher" in data["coredata"]:
                publisher_name = data["coredata"]["dc:publisher"]
                
            paper_id = "Not Found"
            paper_id = data["coredata"]["eid"]
            title_of_paper = data["coredata"]["dc:title"]
            name_of_journal = data["coredata"]["prism:publicationName"]
            citation_count = data["coredata"]["citedby-count"]
            date_of_publication = data["coredata"]["prism:coverDate"]
            page_number = data["coredata"]["prism:startingPage"]

            scopus_indexed = "Yes"
            wos_indexed = "Not available in API"
            scopus_quartile = "Not available in API"
            wos_impact_factors = "Not available in API"
            volume_number = "Not available in API"
            issue_number = "Not available in API"

            # Pass data to template context
            return render(request, 'main_form.html', {
                'author_ids': author_ids,
                'author_names': author_names,
                'publisher_id': publisher_id,
                'publisher_name': publisher_name,
                'paper_id': paper_id,
                'doi_id': doi_id,
                'title_of_paper': title_of_paper,
                'name_of_journal': name_of_journal,
                'scopus_indexed': scopus_indexed,
                'wos_indexed': wos_indexed,
                'scopus_quartile': scopus_quartile,
                'wos_impact_factors': wos_impact_factors,
                'volume_number': volume_number,
                'issue_number': issue_number,
                'page_number': page_number,
                'date_of_publication': date_of_publication,
                'citation_count': citation_count,
            })
        else:
            return render(request, 'error_template.html', {'error': 'Failed to fetch data from the API'})

    return render(request, 'doi_form.html')