from mongoengine import Document, StringField, DateTimeField, DictField

class App(Document):
    app_name = StringField(required=True)
    customer = StringField()
    wayleave_date = DateTimeField()
    in_design_date = DateTimeField()
    usp_date = DateTimeField()
    passed_date = DateTimeField()
    current_stage = StringField(choices=[
        'wayleave', 'in_design', 'usp', 'passed'
    ])
    remarks = StringField()
    meta = {'collection': 'apps'}

class CivilPack(Document):
    ss_number = StringField(required=True)
    substation_number = StringField()
    job_code = StringField()
    scheme_reference = StringField()
    wayleave_number = StringField()
    passed_date = DateTimeField()
    road_level_number = StringField()
    plot_number = StringField()
    substation_tx_count = StringField()
    waylvb_count = StringField()
    tx_size = StringField()
    meta = {'collection': 'civilpacks'}
