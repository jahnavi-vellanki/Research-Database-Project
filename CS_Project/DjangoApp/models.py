from django.db import models

class User(models.Model):
    MAHEID = models.CharField(primary_key=True, max_length=50)
    Password = models.CharField(max_length=255)

    def __str__(self):
        return self.MAHEID

class Author(models.Model):
    AuthorID = models.AutoField(primary_key=True)
    MAHEID = models.ForeignKey(User, on_delete=models.CASCADE)
    AuthorName = models.CharField(max_length=255)

    def __str__(self):
        return self.AuthorName

class Publisher(models.Model):
    PublisherID = models.AutoField(primary_key=True)
    PublisherName = models.CharField(max_length=255)

    def __str__(self):
        return self.PublisherName

class Paper(models.Model):
    PaperID = models.AutoField(primary_key=True)
    PublisherID = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    DOI = models.CharField(max_length=255, unique=True)
    Title = models.CharField(max_length=255)
    JournalName = models.CharField(max_length=255)
    ScopusIndexed = models.BooleanField(default=False)
    WOSIndexed = models.BooleanField(default=False)
    ScopusQuartile = models.CharField(max_length=10, blank=True, null=True)
    WOSImpactFactors = models.CharField(max_length=255, blank=True, null=True)
    VolumeNumber = models.IntegerField(blank=True, null=True)
    IssueNumber = models.IntegerField(blank=True, null=True)
    PageNumber = models.CharField(max_length=50, blank=True, null=True)
    DateOfPublication = models.DateField(blank=True, null=True)
    CitationCount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.Title

class Authored(models.Model):
    ID = models.AutoField(primary_key=True)
    AuthorID = models.ForeignKey(Author, on_delete=models.CASCADE)
    PaperID = models.ForeignKey(Paper, on_delete=models.CASCADE)
