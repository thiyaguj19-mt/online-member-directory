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
    id = models.IntegerField(primary_key=True)
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
    gender = models.CharField(max_length=1, choices=GENGERCHOICES, default='', help_text='Member Gender', blank=True)
    email = models.EmailField(max_length=30, help_text='Member Email', primary_key=True, null=False)
    phone = models.BigIntegerField(help_text='Member Phone')
    address_1 = models.CharField(max_length=150, help_text='Member Address_1', null=True, blank=True)
    address_2 = models.CharField(max_length=150, help_text='Member Address_2', null=True, blank=True)
    city = models.CharField(max_length=60, help_text='Member City')
    zip_code = models.CharField(max_length=10, help_text='Member zip_code', null=True, blank=True)
    state = models.CharField(max_length=30, help_text='Member state')
    country = models.CharField(max_length=30, help_text='Member country', default='USA')
    AGEGROUPCHOICES = [
        ('SSE', 'SSE (4 - 8)'),
        ('YA', 'YA (18 - 40)'),
        ('Adult', 'Adult (40 +)'),
        ('', 'Not Specified'),
    ]
    age_group = models.CharField(max_length=10, choices=AGEGROUPCHOICES, default='', blank=True)
    MEMBERCHOICES = [
        (0, 'Pending_Approval'),
        (1, 'Approved'),
    ]
    member_status = models.IntegerField(choices=MEMBERCHOICES, default=0, help_text='member status')
    orgrole = models.ManyToManyField(OrgRole, help_text='select organization role')
    approle = models.ForeignKey(AppRole, on_delete=models.CASCADE)
    start_date = models.DateField(help_text="Member's OrgRole Start Date", blank=True, null=True)
    end_date = models.DateField(help_text="Member's OrgRole End Date", blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True)

    def get_orgrole(self):
        return " | ".join([orgtitle.name for orgtitle in self.orgrole.all()])

    get_orgrole.short_description = 'Org Title'

    class Meta:
        ordering = ['first_name']
        permissions = (
                        ("is_central_officer", "is central officer"),
                        ("is_regional_officer", "is regional officer"),
                        ("is_national_officer", "is national officer"),
                        #("can_modify_member_data", "to modify member data"),
                    )
