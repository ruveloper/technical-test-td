from fastapi import APIRouter
from fastapi import Depends

from app.auth import auth_service
from app.database.models import (
    Participant,
    Participant_Pydantic,
    Process,
    Process_Pydantic,
    ProcessDetail,
    ProcessDetail_Pydantic,
    Proceeding,
    Proceeding_Pydantic,
)

router = APIRouter(
    prefix="/api",
    dependencies=[Depends(auth_service.manager)],
)


# * DATA API VIEWS


@router.get("/participants", response_model=list[Participant_Pydantic])
async def get_participants():
    return await Participant_Pydantic.from_queryset(Participant.all())


@router.get("/participants/{participant_id}", response_model=Participant_Pydantic)
async def get_participant(participant_id: int):
    return await Participant_Pydantic.from_queryset_single(Participant.get(id=participant_id))


@router.get("/participants/{participant_id}/processes", response_model=list[Process_Pydantic])
async def get_processes(participant_id: int):
    participant = await Participant.get(id=participant_id)
    return await Process_Pydantic.from_queryset(Process.filter(participant=participant))


@router.get("/processes", response_model=list[Process_Pydantic])
async def get_processes():
    return await Process_Pydantic.from_queryset(Process.all())


@router.get("/processes/{process_id}", response_model=Process_Pydantic)
async def get_process(process_id: int):
    return await Process_Pydantic.from_queryset_single(Process.get(id=process_id))


@router.get("/processes/{process_id}/process-details", response_model=list[ProcessDetail_Pydantic])
async def get_process_details(process_id: int):
    process = await Process.get(id=process_id)
    return await ProcessDetail_Pydantic.from_queryset(ProcessDetail.filter(process=process))


@router.get("/process-details", response_model=list[ProcessDetail_Pydantic])
async def get_process_details():
    return await ProcessDetail_Pydantic.from_queryset(ProcessDetail.all())


@router.get("/process-details/{process_detail_id}", response_model=ProcessDetail_Pydantic)
async def get_process_detail(process_detail_id: int):
    return await ProcessDetail_Pydantic.from_queryset_single(ProcessDetail.get(id=process_detail_id))


@router.get("/process-details/{process_detail_id}/proceedings", response_model=list[Proceeding_Pydantic])
async def get_proceedings(process_detail_id: int):
    process_detail = await ProcessDetail.get(id=process_detail_id)
    return await Proceeding_Pydantic.from_queryset(Proceeding.filter(process_detail=process_detail))
