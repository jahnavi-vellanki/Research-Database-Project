import requests
from django.shortcuts import render
from .models import Paper
from dotenv import load_dotenv
import os
import django_tables2 as tables
from .tables import PaperTable
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_tables2.export.views import ExportMixin

# def author_detail(request, author_id):
#     author = Author.objects.get(AuthorID=author_id)
#     authored_papers = author.authored_set.all()
#     context = {
#         'author': author,
#         'authored_papers': authored_papers
#     }
#     return render(request, 'author_detail.html', context)

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

@method_decorator(login_required, name='dispatch')
class PapersListView(ExportMixin, tables.SingleTableView):
    model = Paper
    table_class = PaperTable
    template_name = 'papers.html'
    

@login_required
def submit_paper(request):
    if request.method == 'POST':
        author_ids = request.POST.get('author_ids')
        doi_id = request.POST.get('doi_id')
        author_names = request.POST.get('author_names')
        publisher_id = request.POST.get('publisher_id')
        publisher_name = request.POST.get('publisher_name')
        paper_id = request.POST.get('paper_id')
        title_of_paper = request.POST.get('title_of_paper')
        name_of_journal = request.POST.get('name_of_journal')
        scopus_indexed = request.POST.get('scopus_indexed')
        wos_indexed = request.POST.get('wos_indexed')
        scopus_quartile = request.POST.get('scopus_quartile')
        wos_impact_factors = request.POST.get('wos_impact_factors')
        volume_number = None if request.POST.get('volume_number') == "" else int(request.POST.get('volume_number'))
        issue_number = None if request.POST.get('issue_number') == "" else int(request.POST.get('issue_number'))
        page_number = None if request.POST.get('page_number') == "" else int(request.POST.get('page_number'))
        date_of_publication = request.POST.get('date_of_publication')
        citation_count = None if request.POST.get('citation_count') == "" else int(request.POST.get('citation_count'))

        paper = Paper(PaperID=paper_id, PublisherName=publisher_name, PublisherID=publisher_id, DOI=doi_id,
        Title=title_of_paper, JournalName=name_of_journal, ScopusIndexed=scopus_indexed, WOSIndexed=wos_indexed,
        ScopusQuartile=scopus_quartile, WOSImpactFactors=wos_impact_factors, VolumeNumber=volume_number, IssueNumber=issue_number,
        PageNumber=page_number, DateOfPublication=date_of_publication, CitationCount=citation_count)
        paper.save()
        return render(request, 'doi_form.html')

@login_required
def main_form(request):
    load_dotenv()
    if request.method == 'GET':
        doi_id = request.GET['doi']
        api_key = os.getenv("SCOPUS_API_KEY")
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

            page_number = ""
            if "prism:startingPage" in data["coredata"]:
                page_number = data["coredata"]["prism:startingPage"]

            scopus_indexed = "True"
            wos_indexed = ""
            scopus_quartile = ""
            wos_impact_factors = ""
            volume_number = ""
            issue_number = ""

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