from django.db import models

class Region(models.Model):

    # Fields
    name = models.CharField(max_length=20, help_text='Region Name')

    # Metadata
    #this metadata is to control the default ordering of records returned when you query the model type
    ordering = ['name']

    # Methods

    def __str__(self):
        return self.name

class Center(models.Model):

    #Fields
    name = models.CharField(max_length=100, help_text='Center Name')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    #metadata
    ordering = ['name']

    # Methods
    def __str__(self):
        return self.name

class OrgRole(models.Model):

    #Fields
    name = models.CharField(max_length=100, help_text='Organization Role Name')
    description = models.CharField(max_length=200, help_text='Organization Role Description')

    #metadata
    ordering = ['name']

    #Methods
    def __str__(self):
        return self.name

class AppRole(models.Model):

    #Fields
    name = models.CharField(max_length=100, help_text='Application Role Name')
    description = models.CharField(max_length=200, help_text='Application Role Description')

    #metadata
    ordering = ['name']

    #Methods
    def __str__(self):
        return self.name


class Member(models.Model):

    #Fields
    first_name = models.CharField(max_length=100, help_text='Member First Name')
    last_name = models.CharField(max_length=100, help_text='Member Last Name')
    gender = models.CharField(max_length=10, help_text='Member Gender')
    email = models.EmailField(max_length=30, help_text='Member Email', primary_key=True, null=False)
    phone = models.BigIntegerField(help_text='Member Phone')
    address = models.CharField(max_length=300, help_text='Member Address', null=True)
    age = models.IntegerField(help_text='Member Age')
    class MemberStatus(models.TextChoices):
        NO = (0, 'No')
        YES = (1, 'Yes')
    verified = models.IntegerField(choices=MemberStatus.choices, default=MemberStatus.NO)
    orgrole = models.ForeignKey(OrgRole, on_delete=models.CASCADE)
    approle = models.ForeignKey(AppRole, on_delete=models.CASCADE)
    start_date = models.DateField(help_text="Member's OrgRole Start Date")
    end_date = models.DateField(help_text="Member's OrgRole End Date")
    center = models.CharField(max_length=100, help_text="Member's Center")
