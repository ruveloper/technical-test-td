from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Participant(models.Model):
    """
    The Base model which includes actors and defendants.
    """

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # * Fields
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=20, delfault="actor")
    identifier = fields.CharField(max_length=50)
    process_count = fields.IntField()

    def __str__(self):
        return self.identifier


Participant_Pydantic = pydantic_model_creator(Participant, name="Participant")


class Process(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # * Fields
    id = fields.IntField(pk=True)
    process_id = fields.IntField()
    date = fields.DateField()
    number = fields.CharField(max_length=50)
    infringement = fields.TextField()

    # * Relations
    participant = fields.ForeignKeyField("models.Participant", related_name="processes")

    def __str__(self):
        return self.number


Process_Pydantic = pydantic_model_creator(Process, name="Process")


class ProcessDetail(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # * Fields
    id = fields.IntField(pk=True)
    dependency = fields.TextField()
    city = fields.CharField(max_length=255)
    number = fields.CharField(max_length=50)
    date = fields.DatetimeField()
    actors = fields.TextField()
    defendants = fields.TextField()

    # * Relations
    process = fields.ForeignKeyField("models.Process", related_name="process_details")

    def __str__(self):
        return self.number


ProcessDetail_Pydantic = pydantic_model_creator(ProcessDetail, name="ProcessDetail")


class Proceeding(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # * Fields
    id = fields.IntField(pk=True)
    date = fields.DatetimeField()
    title = fields.TextField()
    content = fields.TextField()

    # * Relations
    process_detail = fields.ForeignKeyField("models.ProcessDetail", related_name="proceedings")

    def __str__(self):
        return self.number


Proceeding_Pydantic = pydantic_model_creator(Proceeding, name="Proceeding")
