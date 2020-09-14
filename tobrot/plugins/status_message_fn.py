#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
import io
import os
import shutil
import sys
import time
import traceback
from tobrot import (
    BOT_START_TIME,
    LOGGER,
    LOG_FILE_ZZGEVC,
    MAX_MESSAGE_LENGTH
)
from tobrot.helper_funcs.download_aria_p_n import (
    aria_start
)
from tobrot.helper_funcs.upload_to_tg import upload_to_tg
from tobrot.dinmamoc import Commandi
from tobrot.amocmadin import Loilacaztion
from tobrot.helper_funcs.display_progress import (
    time_formatter,
    humanbytes
)


async def status_message_f(client, message):
    aria_i_p = await aria_start()
    # Show All Downloads
    downloads = aria_i_p.get_downloads()
    #
    DOWNLOAD_ICON = "📥"
    UPLOAD_ICON = "📤"
    #
    msg = ""
    for download in downloads:
        msg += f"<u>{download.name}</u> |" \
            f"{download.total_length_string()} |" \
            f"{download.progress_string()} |" \
            f"{DOWNLOAD_ICON} {download.download_speed_string()} |" \
            f"{UPLOAD_ICON} {download.upload_speed_string()} |" \
            f"{download.eta_string()}" \
            f"{download.status} |" \
            f"<code>{Commandi.CANCEL} {download.gid}</code> |"
        msg += "\n\n"
    # LOGGER.info(msg)

    if msg == "":
        msg = Loilacaztion.NO_TOR_STATUS

    currentTime = time_formatter((time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")

    ms_g = f"<b>Bot Uptime</b>: <code>{currentTime}</code>\n" \
        f"<b>Total disk space</b>: <code>{humanbytes(total)}</code>\n" \
        f"<b>Used</b>: <code>{humanbytes(used)}</code>\n" \
        f"<b>Free</b>: <code>{humanbytes(free)}</code>\n"

    msg = ms_g + "\n" + msg
    await message.reply_text(msg, quote=True)


async def cancel_message_f(client, message):
    if len(message.command) > 1:
        # /cancel command
        i_m_s_e_g = await message.reply_text(
            Loilacaztion.PROCESSING,
            quote=True
        )
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        try:
            downloads = aria_i_p.get_download(g_id)
            LOGGER.info(downloads)
            LOGGER.info(downloads.remove(force=True, files=True))
            await i_m_s_e_g.edit_text(
                Loilacaztion.TOR_CANCELLED
            )
        except Exception as e:
            LOGGER.warn(str(e))
            await i_m_s_e_g.edit_text(
                Loilacaztion.TOR_CANCEL_FAILED
            )
    else:
        await message.delete()


async def exec_message_f(client, message):
    # DELAY_BETWEEN_EDITS = 0.3
    # PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

    # start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "😐"
    o = stdout.decode()
    if not o:
        o = "😐"
    OUTPUT = ""
    OUTPUT += "<b>EXEC:</b>\n" \
        f"<u>Command:</u> <code>{cmd}</code>\n" \
        f"<u>PID</u>: <code>{process.pid}</code>\n" \
        f"<b>stderr:</b>\n<code>{e}</code>\n" \
        f"<b>stdout:</b>\n<code>{o}</code>\n" \
        f"<b>return:</b> <code>{process.returncode}</code>"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await client.send_document(
            chat_id=message.chat.id,
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("exec.text")
        await message.delete()
    else:
        await message.reply_text(OUTPUT)


async def upload_document_f(client, message):
    imsegd = await message.reply_text(
        Loilacaztion.PROCESSING
    )
    if " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        recvd_response = await upload_to_tg(
            imsegd,
            local_file_name,
            message.from_user.id,
            {}
        )
        LOGGER.info(recvd_response)
    await imsegd.delete()


async def save_rclone_conf_f(client, message):
    chat_type = message.chat.type
    r_clone_conf_uri = None
    if chat_type in ["private", "bot", "group"]:
        r_clone_conf_uri = f"https://t.me/PublicLeech/{message.chat.id}/{message.reply_to_message.message_id}"
    elif chat_type in ["supergroup", "channel"]:
        if message.chat.username:
            r_clone_conf_uri = "please DO NOT upload confidential credentials, in a public group."
        else:
            r_clone_conf_uri = f"https://t.me/c/{str(message.reply_to_message.chat.id)[4:]}/{message.reply_to_message.message_id}"
    else:
        r_clone_conf_uri = "unknown chat_type"
    await message.reply_text(
        "<code>"
        f"{r_clone_conf_uri}"
        "</code>"
    )


async def upload_log_file(client, message):
    await message.reply_document(
        LOG_FILE_ZZGEVC
    )


async def eval_message_f(client, message):
    ismgese = await message.reply_text("...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc.strip()
    elif stderr:
        evaluation = stderr.strip()
    elif stdout:
        evaluation = stdout.strip()
    else:
        evaluation = "😐"

    final_output = ""
    final_output += f"<b>EVAL</b>: <code>{cmd}</code>"
    final_output += "\n\n<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation}</code>\n"

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await ismgese.reply_document(
            document="eval.text",
            caption=cmd
        )
        os.remove("eval.text")
        await ismgese.delete()
    else:
        await ismgese.edit(final_output)


async def aexec(code, client, message):
    exec(
        'async def __aexec(client, message): ' +
        ''.join(f'\n {line}' for line in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)
