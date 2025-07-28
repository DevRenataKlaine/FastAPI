from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))
    user_dict = asdict(user)

    assert user_dict['id'] == 1
    assert user_dict['username'] == 'alice'
    assert user_dict['password'] == 'secret'
    assert user_dict['email'] == 'teste@test'
    assert user_dict['created_at'] == time
    assert user_dict['todos'] == []

    # Valida 'updated_at' de forma flexível
    assert 'updated_at' not in user_dict or user_dict[
        'updated_at'
    ] in {None, time}


@pytest.mark.asyncio
async def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',  # type: ignore
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()

    todo = await session.scalar(select(Todo))

    todo_dict = asdict(todo)
    assert todo_dict['description'] == 'Test Desc'
    assert todo_dict['id'] == 1
    assert todo_dict['state'] == 'draft'
    assert todo_dict['title'] == 'Test Todo'
    assert todo_dict['user_id'] == 1


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',  # type: ignore
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))
    assert user.todos == [todo]
