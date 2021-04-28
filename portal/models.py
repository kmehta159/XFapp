from django.db import models

# Create your models here.
class xftool(models.Model):
    tool_id = models.AutoField
    tool_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    AG_LEARN = "Agilent Learning"
    INST_QC = "Instrument QC"
    CAR_QC = "Cartridge QC"
    SPOTTING = "Spotting"
    METROLOGY = "Metrology"
    department_list = ((AG_LEARN, 'Agilent Learning'), (INST_QC,'Instrument QC'), (CAR_QC,'Cartridge QC'),
                       (SPOTTING, 'Spotting'), (METROLOGY, 'Metrology'))
    department = models.CharField(max_length=50, choices= department_list, default='Agilent Learning')
    category = models.CharField(max_length=50, default='')
    subcategory = models.CharField(max_length=200, default='')
    pub_date = models.DateField()
    image = models.ImageField(upload_to="tools/images", default="")

    def __str__(self):
        return self.tool_name