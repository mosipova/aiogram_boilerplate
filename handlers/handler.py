from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext

from templates.commands import cmd_help, cmd_test
from templates.messages import START_MESSAGE, HELP_MESSAGE

from aiogram.utils.markdown import hbold

router = Router()


class TestFlow(StatesGroup):
    wait_for_answer = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await state.clear()
    await message.answer(hbold(START_MESSAGE))


@router.message(Command(cmd_help))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer(HELP_MESSAGE)


@router.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


# handlers illustrating State workflow
# comment echo_handler to test
@router.message(Command(commands=[cmd_test]))
async def command_test_handler(message: Message, state: FSMContext):
    await state.clear()
    test_flow_message = f'test state initiated at {message.date}'
    await state.update_data(test_data=test_flow_message)
    await state.set_state(TestFlow.wait_for_answer.state)
    await message.answer(f'{test_flow_message}')


@router.message(StateFilter(TestFlow.wait_for_answer))
async def test_state_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f'{data['test_data']} interrupted at {message.date}')
    await state.set_state(state=None)
