from datetime import datetime
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlmodel import Session, select

from configs.db import get_session
from models.vm import VM, VMCreate, VMRead, VMUpdate
from utils.deps import get_current_user, require_administrator
from utils.ws_broadcaster import manager

router = APIRouter(
    prefix="/vms",
    tags=["vms"],
    dependencies=[Depends(get_current_user)]  # todas requieren token válido
)

@router.get("/", response_model=List[VMRead])
def list_vms(
    session: Session = Depends(get_session),
):
    return session.exec(select(VM)).all()

@router.get("/{vm_id}", response_model=VMRead)
def get_vm(
    *,
    vm_id:  int,
    session: Session = Depends(get_session),
):
    vm = session.get(VM, vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="VM no encontrada")
    return vm

@router.post("/", response_model=VMRead, status_code=status.HTTP_201_CREATED)
def create_vm(
    *,
    payload: VMCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    _:   any     = Depends(require_administrator),  # sólo administrador
):
    vm = VM(**payload.dict())
    session.add(vm)
    session.commit()
    session.refresh(vm)
    # 4) Publicamos el evento en background para no bloquear
    # 🚀 emitimos evento “user_created”
    background_tasks.add_task(
        manager.broadcast,
        {
            "event": "user_created",
            "user": VMRead.from_orm(vm).dict(),
        },
    )
    return vm



@router.put("/{vm_id}", response_model=VMRead)
def update_vm(
    *,
    vm_id:  int,
    payload: VMUpdate,
    session: Session = Depends(get_session),
    _:   any     = Depends(require_administrator),
):
    vm = session.get(VM, vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="VM no encontrada")
    data = payload.dict(exclude_unset=True)
    # actualizamos campos y timestamp
    for k, v in data.items():
        setattr(vm, k, v)
    vm.updated_at = datetime.utcnow()
    session.add(vm)
    session.commit()
    session.refresh(vm)
    return vm

@router.delete("/{vm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vm(
    *,
    vm_id: int,
    session: Session = Depends(get_session),
    _:   any = Depends(require_administrator),
):
    vm = session.get(VM, vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="VM no encontrada")
    session.delete(vm)
    session.commit()

