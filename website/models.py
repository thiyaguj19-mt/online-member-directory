from django.db import models

class Region(models.Model):

    # Fields
    name = models.CharField(max_length=20, help_text='Region Name')

    # Metadata
    #this metadata is to control the default ordering of records returned when you query the model type
    #ordering = ['name']

    # Methods

    def __str__(self):
        return self.name

class Center(models.Model):

    #Fields
    name = models.CharField(max_length=100, help_text='Center Name')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    #metadata
    #ordering = ['name']

    # Methods
    def __str__(self):
        return self.name

class OrgRole(models.Model):

    #Fields
    name = models.CharField(max_length=100, help_text='Organization Role Name')
    description = models.CharField(max_length=200, help_text='Organization Role Description', blank=True)

    #metadata
    ordering = ['name']

    #Methods
    def __str__(self):
        return self.name

class AppRole(models.Model):

    #Fields
    name = models.CharField(max_length=100, help_text='Application Role Name')
    level = models.CharField(max_length=2, help_text='access level', default="L1")
    description = models.CharField(max_length=200, help_text='Application Role Description', blank=True)

    #metadata
    ordering = ['name']

    #Methods
    def __str__(self):
        return self.name

class Metadata(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=600)

    def __str__(self):
        return f'{self. key} | {self.value}'

class Member(models.Model):

    #Fields
    first_name = models.CharField(max_length=100, help_text='Member First Name')
    last_name = models.CharField(max_length=100, help_text='Member Last Name')
    GENGERCHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('', 'Not Specified'),
    ]
    gender = models.CharField(max_length=1, choices=GENGERCHOICES, default='', help_text='Choose Member Gender')
    email = models.EmailField(max_length=30, help_text='Member Email', primary_key=True, null=False)
    phone = models.BigIntegerField(help_text='Member Phone')
    address = models.CharField(max_length=300, help_text='Member Address', null=True, blank=True)
    age = models.CharField(max_length=3, help_text='Member Age', blank=True)
    MEMBERCHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    verified = models.IntegerField(choices=MEMBERCHOICES, default=0, help_text='member status')
    orgrole = models.ManyToManyField(OrgRole, help_text='select organization role')
    approle = models.ForeignKey(AppRole, on_delete=models.CASCADE)
    start_date = models.DateField(help_text="Member's OrgRole Start Date", blank=True, null=True)
    end_date = models.DateField(help_text="Member's OrgRole End Date", blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, blank=True, null=True)

    def get_orgrole(self):
        return " | ".join([orgtitle.name for orgtitle in self.orgrole.all()])

    get_orgrole.short_description = 'Org Title'
