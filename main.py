from aiogram import Bot, Dispatcher, F, types
import asyncio
import logging
import sqlite3
import os
import datetime
import time
from aiogram.utils.keyboard import InlineKeyboardBuilder
import string
import random
from PIL import ImageColor, Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps, ImageChops
from aiogram.types import FSInputFile, BufferedInputFile, LabeledPrice
import zipfile
from pathlib import Path
import numpy as np
import shutil
import io
import matplotlib.colors as mcolors
from concurrent.futures import ThreadPoolExecutor
import aiofiles
from aiogram.types.input_media_document import InputMediaDocument
import json
from txd import TXDConverter
import re
from shutil import rmtree
import struct
from skimage.measure import label, regionprops
from skimage.morphology import disk, closing, opening
from skimage import exposure
from skimage.filters import threshold_otsu
from scipy.ndimage import gaussian_filter
from pyrogram import Client, enums
from telethon import TelegramClient, events, Button
from groq import Groq
import colorsys
from sklearn.cluster import KMeans
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("TOKEN")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
p_app = Client("pyro_download_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
t_client = TelegramClient("tele_upload_session", API_ID, API_HASH)
logging.basicConfig(level=logging.INFO)
loging_id = [2080411409]
boti = Bot(token=os.getenv("token2"))
length = 4
DB_PATH = 'users.db'
BOT_NAME = "Pweper Bot"
BOT_USERNAME = "pweper_bot"
SUPPORT_USERNAME = "keedboy016"
GROQ_RATE_LIMIT_PER_MIN = 10
FREE_TRIAL_STARS = 1
FREE_TRIAL_DAYS = 3
FREE_TRIAL_FREE_REFS = 25

FREE_MAX_FILE_MB = 20
FREE_DELAY_SEC = 2
MAX_WORK_SIZE_GB = 1.5
FREE_TIMEOUT_SEC = 60  # seconds before warning free users
ANTISPAM_WINDOW = 10
ANTISPAM_LIMIT = 6
ANTISPAM_BLOCK_SEC = 45
FILE_ANTISPAM_WINDOW = 10
FILE_ANTISPAM_LIMIT = 4
FILE_ANTISPAM_BLOCK_SEC = 30
DEFAULT_CHANNELS = ['@pweper', '@nonerai', '@noberai_team']

SUBSCRIPTION_PLANS = [
    {"stars": 50, "days": 14, "label": "2 недели", "emoji": "⚡"},
    {"stars": 80, "days": 30, "label": "1 месяц", "emoji": "🔥"},
    {"stars": 200, "days": 90, "label": "3 месяца", "emoji": "💎"},
    {"stars": 350, "days": 180, "label": "6 месяцев", "emoji": "👑"},
    {"stars": 600, "days": 365, "label": "1 год", "emoji": "🏆"},
    {"stars": 1000, "days": -1, "label": "Навсегда", "emoji": "♾️"},
]

FILE_SUFFIXES = ['logobrkrasnodar', 'logobrkaliningrad', 'logobrbelgorod', 'logobrizhevsk', 'logobrgray',
                 'logobryakutsk', 'logobrvoronezh', 'logobrcherry', 'logobrcrimson', 'logobrkrasnoyarsk',
                 'logobrnorilsk', 'logobrorel', 'logobrbratsk', 'logobrlipetsk', 'logobrtolyatti', 'logobrcherepovets',
                 'logobrkirov', 'logobrkostroma', 'logobrspb', 'logobrastrakhan', 'logobrarkhangelsk',
                 'logobrstavropol', 'logobrvladivostok', 'logobrmagenta', 'logobrbarnaul', 'logobrmoscow',
                 'logobrvladimir', 'logobrrostov', 'logobraqua', 'logobrsochi', 'logobrarzamas', 'logobryellow',
                 'logobrnovgorod', 'logobrchelyabinsk', 'logobrorange', 'logobrkazan', 'logobrpodolsk',
                 'logobrkhabarovsk', 'logobrsaratov', 'logobrtver', 'logobranapa', 'logobrvologda', 'logobrkemerovo',
                 'logobrchita', 'logobrgreen', 'logobryaroslavl', 'logobrchoco', 'logobrmakhachkala', 'logobrpskov',
                 'logobrgrozny', 'logobrtambov', 'logobrekb', 'logobrcheboksary', 'logobrvladikavkaz', 'logo',
                 'logobrmagadan', 'logobrred', 'logobrplatinum', 'logobrsmolensk', 'logobrwhite', 'logobrvolgograd',
                 'logobrpurple', 'logobrnovosib', 'logobrtula', 'logobrtaganrog', 'logobrmurmansk', 'logobrsurgut',
                 'logobrufa', 'logobrblack', 'logobrchilli', 'logobrlime', 'logobrperm', 'logobromsk', 'logobrazure',
                 'logobrice', 'logobrbryansk', 'logobrkursk', 'logobrryazan', 'logobrpenza', 'logobrirkutsk',
                 'logobrblue', 'logobrsamara', 'logobrindigo', 'logobrkaluga', 'logobrtyumen', 'logobrorenburg',
                 'logobrgold', 'logobrulyanovsk', 'logobrpink', 'logobrtomsk', 'logobrivanovo']
MAX_FILE_SIZE = 1024 * 1024 * 50
Tree = ['417f945c', '43tree1', '43tree2', '43tree3', '43tree4', '43tree5', '43tree6', '43tree7', '43tree8', '43tree9',
        '44tree1', '44tree2', '44tree4', '44tree5', '9event_treesbg1', '9event_treesbg2', 'apat_flowers', 'AppleTree',
        'AucTreeCrone8712', 'AucWeed8163', 'Bdup2_plant', 'beregd1_elka', 'beregd1_listv2', 'BRG_flowers1',
        'BRTREE_Atl_B', 'BRTREE_leaf1', 'BRTREE_leaf1o', 'BRTREE_leaf2', 'BRTREE_leaf2o', 'BRTREE_leaf3',
        'BRTREE_leaf4', 'BRTREE_leaf4o', 'BRTREE_leaf5', 'BRTREE_leaf5o', 'BRTREE_leaf6', 'BRTREE_leaf7',
        'BRTREE_leaf8', 'BRTREE_leaf8o', 'BukTree1', 'BukTree2', 'bysaevo_grasssandmix', 'byssch_flower1',
        'byssch_flower2', 'byssch_flower3', 'byssch_flower4', 'byssch_flower5', 'bys_appletree', 'bys_cherrytree',
        'bys_flowers', 'bys_plumtree', 'bys_wires', 'b_craet1_4_ca', 'cactusL', 'CasinoNor3864',
        'cj_flower(hi_res)cj_flower_a(h', 'CJ_FLOWER_256cj_flower_a', 'cj_leaf_cheesecj_leaf_cheese_a', 'CJ_PLANT',
        'cottagetuya-2', 'cottagetuya', 'derevachkacrb', 'derevo', 'derevo3', 'derevoclub8201', 'derevoclub8201st',
        'derevoclub82021', 'derevoclub82022', 'derevoclub8202st', 'derevoclub8203', 'derevoclub8203st', 'derevopar7901',
        'derevopar7902', 'derevopar7903', 'derevopar7904', 'derevopar7905', 'derevo_krov', 'edovo_coundom_flower', 'f',
        'fialkiflowers', 'flowert', 'free grass', 'freegrass', 'gameleaf01_64', 'gameleaf02_64', 'grass1',
        'GrassAlpha7453', 'GrassA_02', 'GrassA_04', 'GrassA_05', 'GrassA_15', 'GrassA_15_1', 'GrassA_16', 'GrassA_20',
        'GrassVazMast', 'Grass_00', 'grass_gen256old', 'grass_green_long', 'grass_green_med',
        'gz_e2_fishleaf01gz_e2_fishleaf', 'gz_e2_fishleaf02gz_e2_fishleaf', 'gz_e2_fishleaf03gz_e2_fishleaf',
        'gz_e2_leaf_cheesegz_e2_leaf_ch', 'hot_flowers1', 'int_fsb_flow1', 'int_fsb_flow1a', 'int_pr_flow1',
        'int_pr_flow2', 'izbamishura', 'kbplanter_plants1', 'kb_balcony_ferns', 'kb_balcony_ferns_genintgeneric',
        'kb_ivy2_256', 'klubnika', 'km_flowerpic2', 'km_plant1', 'kolosya_rog', 'KOR_grape', 'krapiva_list', 'kustik1',
        'kustik2', 'KustRog8716', 'kust_farm1', 'kyst3', 'l', 'lager_trees1', 'lager_trees2', 'lag_reeds1',
        'LeavesTropical0141_1', 'LeavesTropical0202_1', 'LeavesTropical0218_1', 'lentisk', 'lf_arzflowers1', 'list4',
        'LODBRTREE_1_6_7_8', 'LODBRTREE_2_3', 'LODBRTREE_4_5_9_10', 'LODBRTREE_atl', 'LODbuktree2_a889',
        'LODbuktree3_a889', 'LODbuktree4_a889', 'LODbuktree5_a889', 'LODbuktree6_a889', 'LODbuktree7_a889',
        'LODbuktree8_a889', 'LODH_leaftree_big', 'LODH_leaftree_med', 'LODH_leaftree_root', 'LODH_leaftree_sml',
        'LODH_leaftree_vol', 'LODH_pinetree1', 'LODH_pinetree2', 'LODH_pinetree3', 'LODH_Rdeadtree', 'lopux_koluchka',
        'lopux_list', 'moss_shrek_a889', 'mp_flowerbush', 'mp_gs_flowerwall', 'mp_h_acc_vase_flowers_04',
        'mp_h_acc_vase_leaves_03mp_h_acc', 'newtreeleaves128', 'newtreeleavesb128', 'NGMishura6121', 'NGMishura6121_2',
        'nonalpha_compressedLOD_treeRUBH', 'NRock_kust1', 'NRock_kust2', 'Palm0471', 'palm8204', 'PalmArecaceae144',
        'PalmWall2947', 'planta252', 'planta256', 'plantc256', 'PlantH1741', 'potato', 'rn_hell_flow',
        'rus_bigORGANGEflower', 'rus_grasstype2', 'rus_grassTYPE3', 'rus_grasstype4_flowers', 'rus_whiteflower_ingrass',
        'R_Berez1_b', 'R_Berez1_t', 'R_Dub1', 'R_hln_MgkLeaf1', 'R_hln_MgkLeaf2', 'R_hln_MgkLeaf3', 'R_Listv1', 'salad',
        'sm_Agave_1', 'sm_Agave_2', 'sm_minipalm1', 'sm_potplant1', 'starflower2', 'starflower2wht', 'starflower3',
        'starflower3prpl', 'starflower3yel', 'Strip_plant', 'stvolListv1', 'svekla', 'tikva', 'tomato', 'TomatoFarm',
        'Tree', 'tree19Mi', 'treeCRB221_1', 'TreeCron9716', 'TreeCron9716_2', 'trees_vetkagreen5', 'treewillow99',
        'tree_lodderevo1', 'tree_lodeubeech1', 'tree_lodfikovnik', 'tree_lodkastan', 'tree_lodlinden',
        'tree_lodpaper_der1', 'tree_lodpaper_der2', 'tree_lodwillow', 'TREE_STUB1', 'tuyaclub8205', 'T_br5_FlwrVs',
        'T_CM_Leaf_D', 'T_flg_Cl_Ch_A', 'T_flg_Cl_Ch_B', 'T_flg_Cl_CrTr_A', 'T_flg_Cl_CrTr_B', 'T_flg_Cl_Dead_A',
        'T_flg_Cl_Hdg_A', 'T_flg_Cl_Lndn_A', 'T_flg_Cl_Mpl_A', 'T_flg_Cl_Poplar_A', 'T_flg_Cl_Shbrr_A',
        'T_flg_Cl_Shbrr_B', 'T_flg_Cl_Th_A', 'T_flg_Cl_Th_B', 'T_flg_Cl_Th_C', 'T_flg_DeadBrunch_A',
        'T_flg_DeadBrunch_B', 'T_flg_ForestGround', 'T_flg_Grss_V', 'T_flg_Grss_V2', 'T_flg_Grss_X', 'T_flg_Grss_Y',
        'T_flg_Hdg_A', 'T_flg_ivy_A', 'T_flg_ivy_fall', 'T_flg_LeafA', 'T_flg_leafs', 'T_flg_Lndn_A_Low',
        'T_flg_Moss_A', 'T_flg_Moss_B', 'T_flg_Moss_C', 'T_flg_NeedleA', 'T_flg_PalmLeaf_A', 'T_flg_ShoreGrassA',
        'T_nn_TreesLODtex_a', 'T_nn_TreesLODtex_b', 'T_nn_TreesLODtex_c', 'UGPRST_der1', 'vk_int_gaz_grass1',
        'vk_m9_ev_kust', 'WH_flowers1', 'yellosmallflowers', 'z-H-dc-Fern1', 'z_H_atl_grss_014']
bild = ['reclam65', 'reclam66', 'Billb_SanVice', 'BLBRD_3_889', 'reclam67', 'BLBRD_1_a889', 'Billb_MyriadIslands',
        'reclam64', 'Billb_AlienCity', 'bilb_sign1', 'BLBRD_btn1_a889', 'BLBRD_5_889', 'reclam69', 'BLBRD_main1_a889',
        'Billb_GTABer', 'reclam68', 'BLBRD_6_889', 'reclam62', 'Billb_GostownParadise', 'reclam63', 'Billb_YouAreHere',
        'bilb_sign2', 'Billb_GTAUnited', 'BLBRD_4_889', 'BLBRD_2_889']

PRESETS = {
    "1": {"name": "Стандарт", "folder": "weapons/presest1", "desc": "Стандартный веапон"},
    "2": {"name": "⚡ Ускор + Антик", "folder": "weapons/presest2", "desc": "Ускоренная стрельба, антикилл, раскрывающийся прицел"},
    "3": {"name": "🔄 Без перезарядки + Динамичный", "folder": "weapons/presest3", "desc": "Без перезарядки, динамичный прицел"},
    "4": {"name": "🎯 Без перезарядки + Статичный", "folder": "weapons/presest4", "desc": "Без перезарядки, статичный прицел"},
}
weapon_user_settings: dict[int, str] = {}

class OverlayStates(StatesGroup):
    waiting_for_second_image = State()

class AdminFSM(StatesGroup):
    broadcast_text = State()
    poll_question = State()
    poll_options = State()
    unban_id = State()
    promo_create = State()
    promo_code_input = State()
    ticket_reply = State()
    ticket_close = State()

class SupportFSM(StatesGroup):
    subject = State()
    message = State()

class BatchFSM(StatesGroup):
    collecting = State()

class BuyFSM(StatesGroup):
    waiting_promo = State()

_active_paid = 0
_active_paid_lock = None
_free_semaphore = None
_paid_semaphore = None

def init_semaphores():
    global _free_semaphore, _paid_semaphore, _active_paid_lock
    _active_paid_lock = asyncio.Lock()
    _free_semaphore = asyncio.Semaphore(2)
    _paid_semaphore = asyncio.Semaphore(8)

async def queue_acquire(is_paid: bool):
    global _active_paid
    if _free_semaphore is None:
        return
    if is_paid:
        async with _active_paid_lock:
            _active_paid += 1
    else:
        if _active_paid > 0:
            await asyncio.sleep(FREE_DELAY_SEC)
        else:
            await asyncio.sleep(2)
        await _free_semaphore.acquire()

async def queue_release(is_paid: bool):
    global _active_paid
    if _free_semaphore is None:
        return
    if is_paid:
        async with _active_paid_lock:
            _active_paid = max(0, _active_paid - 1)
    else:
        _free_semaphore.release()

async def run_with_timeout(coro, timeout_sec: float, user_id: int,
                           is_paid: bool, is_large_file: bool = False):
    """Run coroutine with timeout; warns free user if too slow."""
    if is_paid or is_large_file:
        return await coro
    try:
        return await asyncio.wait_for(coro, timeout=timeout_sec)
    except asyncio.TimeoutError:
        try:
            await bot.send_message(
                user_id,
                "⏱ <b>Превышено время обработки!</b>\n\n"
                "Запрос занял слишком много времени.\n"
                "💎 Для снятия ограничений купите <b>Premium</b>.",
                parse_mode="HTML")
        except Exception:
            pass
        raise

def check_antispam(user_id: int, is_paid: bool = False):
    if is_paid:
        return True, 0.0
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = time.time()
    c.execute("SELECT window_start, msg_count, blocked_until FROM antispam WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        ws, mc, bu = row
        if bu and now < bu:
            conn.close()
            return False, bu
        if now - ws < ANTISPAM_WINDOW:
            mc += 1
            if mc > ANTISPAM_LIMIT:
                new_bu = now + ANTISPAM_BLOCK_SEC
                c.execute("UPDATE antispam SET msg_count=?, blocked_until=? WHERE user_id=?", (mc, new_bu, user_id))
                conn.commit(); conn.close()
                return False, new_bu
            c.execute("UPDATE antispam SET msg_count=? WHERE user_id=?", (mc, user_id))
        else:
            c.execute("UPDATE antispam SET window_start=?, msg_count=1, blocked_until=0 WHERE user_id=?", (now, user_id))
    else:
        c.execute("INSERT INTO antispam (user_id, window_start, msg_count) VALUES (?,?,1)", (user_id, now))
    conn.commit(); conn.close()
    return True, 0.0

def check_file_antispam(user_id: int, is_paid: bool = False):
    if is_paid:
        return True, 0.0
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = time.time()
    c.execute("SELECT file_window_start, file_count, file_blocked_until FROM antispam WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        ws, fc, bu = row
        if bu and now < bu:
            conn.close()
            return False, bu
        if now - ws < FILE_ANTISPAM_WINDOW:
            fc += 1
            if fc > FILE_ANTISPAM_LIMIT:
                new_bu = now + FILE_ANTISPAM_BLOCK_SEC
                c.execute("UPDATE antispam SET file_count=?, file_blocked_until=? WHERE user_id=?", (fc, new_bu, user_id))
                conn.commit(); conn.close()
                return False, new_bu
            c.execute("UPDATE antispam SET file_count=? WHERE user_id=?", (fc, user_id))
        else:
            c.execute("UPDATE antispam SET file_window_start=?, file_count=1, file_blocked_until=0 WHERE user_id=?", (now, user_id))
    else:
        c.execute("INSERT OR IGNORE INTO antispam (user_id, file_window_start, file_count) VALUES (?,?,1)", (user_id, now))
        c.execute("UPDATE antispam SET file_window_start=?, file_count=1, file_blocked_until=0 WHERE user_id=?", (now, user_id))
    conn.commit(); conn.close()
    return True, 0.0

def get_required_channels():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT channel_username FROM required_channels")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def add_channel(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO required_channels (channel_username, channel_name) VALUES (?,?)", (username, username))
    conn.commit(); conn.close()

def remove_channel(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM required_channels WHERE channel_username=?", (username,))
    ok = c.rowcount > 0
    conn.commit(); conn.close()
    return ok

async def check_required_subs(user_id: int):
    not_sub = []
    for ch in get_required_channels():
        try:
            m = await bot.get_chat_member(ch, user_id)
            if m.status in ("left", "kicked"):
                not_sub.append(ch)
        except Exception as e:
            logging.warning(f"check_required_subs {ch}: {e}")
    return not_sub

def is_banned(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT banned, ban_reason FROM users WHERE chat_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == 'True':
        return True, row[1]
    return False, None

def ban_user(user_id: int, reason: str = "Нарушение правил"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET banned='True', ban_reason=? WHERE chat_id=?", (reason, user_id))
    conn.commit(); conn.close()

def unban_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET banned='False', ban_reason=NULL WHERE chat_id=?", (user_id,))
    conn.commit(); conn.close()

def inc_msg_count(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    c.execute("UPDATE users SET msg_count=COALESCE(CAST(msg_count AS INTEGER),0)+1, last_active=? WHERE chat_id=?", (now, user_id))
    conn.commit(); conn.close()

def get_top_users(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chat_id, username, COALESCE(CAST(msg_count AS INTEGER),0) FROM users WHERE banned!='True' ORDER BY CAST(msg_count AS INTEGER) DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_bot_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users"); total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE sub='True'"); paid = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE banned='True'"); banned = c.fetchone()[0]
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    c.execute("SELECT COUNT(*) FROM users WHERE last_active LIKE ?", (f"{today}%",)); today_active = c.fetchone()[0]
    conn.close()
    return {"total": total, "paid": paid, "free": total-paid, "banned": banned, "today": today_active}

def get_work_size_gb():
    total = 0
    p = Path('work')
    if not p.exists(): return 0.0
    for f in p.rglob('*'):
        if f.is_file():
            try: total += f.stat().st_size
            except: pass
    return total / (1024 ** 3)

async def auto_cleanup():
    if get_work_size_gb() < MAX_WORK_SIZE_GB:
        return
    logging.warning(f"[cleanup] work/ > {MAX_WORK_SIZE_GB} GB, чищу...")
    work = Path('work')
    dirs = []
    for d in work.rglob('*'):
        if d.is_dir() and d != work:
            try: dirs.append((d.stat().st_mtime, d))
            except: pass
    dirs.sort(key=lambda x: x[0])
    for _, d in dirs:
        if get_work_size_gb() < MAX_WORK_SIZE_GB * 0.6:
            break
        shutil.rmtree(d, ignore_errors=True)

def save_invoice(payload: str, user_id: int, stars: int, days: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO pending_invoices (payload,user_id,stars,days,created_at) VALUES (?,?,?,?,?)",
              (payload, user_id, stars, days, datetime.datetime.now().isoformat()))
    conn.commit(); conn.close()

def pop_invoice(payload: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, stars, days FROM pending_invoices WHERE payload=?", (payload,))
    row = c.fetchone()
    if row:
        c.execute("DELETE FROM pending_invoices WHERE payload=?", (payload,))
    conn.commit(); conn.close()
    return row

def grant_subscription(user_id: int, days: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if days == -1:
        expiry = "31.12.2099"
    else:
        expiry = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%d.%m.%Y")
    c.execute("UPDATE users SET sub='True', time=? WHERE chat_id=?", (expiry, user_id))
    conn.commit(); conn.close()
    return expiry

def create_promo(code, name, comment, link, discount_pct, custom_stars,
                 custom_days, max_uses, expires_at, created_by):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    try:
        c.execute("""INSERT INTO promo_codes
            (code,name,comment,link,discount_pct,custom_stars,custom_days,
             max_uses,expires_at,is_active,created_by,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,1,?,?)""",
            (code.upper(), name, comment, link, discount_pct, custom_stars,
             custom_days, max_uses, expires_at, created_by, now))
        conn.commit(); conn.close()
        return True, None
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Промокод уже существует"

def get_promo(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM promo_codes WHERE code=? AND is_active=1", (code.upper(),))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    keys = ["id","code","name","comment","link","discount_pct","custom_stars",
            "custom_days","max_uses","uses","expires_at","is_active","created_by","created_at"]
    return dict(zip(keys, row))

def list_promos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT code,name,discount_pct,custom_stars,custom_days,uses,"
              "max_uses,expires_at,is_active FROM promo_codes ORDER BY id DESC")
    rows = c.fetchall(); conn.close()
    return rows

def deactivate_promo(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE promo_codes SET is_active=0 WHERE code=?", (code.upper(),))
    ok = c.rowcount > 0; conn.commit(); conn.close()
    return ok

def use_promo(code, user_id):
    p = get_promo(code)
    if not p:
        return False, None, "❌ Промокод не найден или неактивен"
    if p["expires_at"]:
        try:
            if datetime.datetime.now() > datetime.datetime.fromisoformat(p["expires_at"]):
                return False, None, "❌ Промокод истёк"
        except:
            pass
    if p["max_uses"] > 0 and p["uses"] >= p["max_uses"]:
        return False, None, "❌ Лимит использований исчерпан"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT active_promo FROM users WHERE chat_id=?", (user_id,))
    existing = c.fetchone()
    if existing and existing[0] and existing[0].upper() != code.upper():
        old_promo = get_promo(existing[0])
        if old_promo:
            c.execute("UPDATE users SET active_promo=NULL, promo_expires=NULL WHERE chat_id=?", (user_id,))
            conn.commit()
    try:
        c.execute("INSERT INTO promo_uses (code,user_id,used_at) VALUES (?,?,?)",
                  (code.upper(), user_id, datetime.datetime.now().isoformat()))
        c.execute("UPDATE promo_codes SET uses=uses+1 WHERE code=?", (code.upper(),))
        c.execute("UPDATE users SET active_promo=?, promo_expires=? WHERE chat_id=?",
                  (code.upper(), p["expires_at"], user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False, None, "❌ Вы уже использовали этот промокод"
    conn.close()
    return True, p, None

def apply_promo_to_plan(plan, promo):
    if promo["custom_stars"] > 0:
        return {**plan,
                "stars": promo["custom_stars"],
                "days": promo["custom_days"] if promo["custom_days"] > 0 else plan["days"],
                "label": plan["label"] + " (промо)",
                "emoji": "🎟"}
    if promo["discount_pct"] > 0:
        new_stars = max(1, int(plan["stars"] * (1 - promo["discount_pct"] / 100)))
        return {**plan,
                "stars": new_stars,
                "label": plan["label"] + " -" + str(promo["discount_pct"]) + "%",
                "emoji": "🎟"}
    return plan

REFERRAL_BONUS_TIERS = [(50, 25), (20, 20), (10, 15), (1, 10)]
REFERRAL_REWARD_PCT = 15
L2_REWARD_TIERS = [(50, 4), (20, 3), (10, 2), (0, 1)]


ROLES = {
    "developer": {"level": 3, "label": "👨‍💻 Разработчик"},
    "admin":     {"level": 2, "label": "🛡 Администратор"},
    "moderator": {"level": 1, "label": "🔧 Модератор"},
}

def get_role(user_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE chat_id=?", (user_id,))
    row = c.fetchone(); conn.close()
    if row and row[0] in ROLES:
        return row[0]
    c2 = sqlite3.connect(DB_PATH)
    cur = c2.cursor()
    cur.execute("SELECT admin FROM users WHERE chat_id=?", (user_id,))
    r2 = cur.fetchone(); c2.close()
    if r2 and r2[0] == "True":
        return "admin"
    return None

def get_role_level(user_id: int) -> int:
    role = get_role(user_id)
    return ROLES.get(role, {}).get("level", 0)

def has_perm(user_id: int, min_role: str) -> bool:
    return get_role_level(user_id) >= ROLES.get(min_role, {}).get("level", 999)

def set_role(user_id: int, role: str, by_id: int):
    if role not in ROLES and role != "none":
        return False
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    new_role = role if role != "none" else None
    new_admin = "True" if role in ("admin", "developer") else "False"
    c.execute("UPDATE users SET role=?, admin=? WHERE chat_id=?", (new_role, new_admin, user_id))
    ok = c.rowcount > 0
    conn.commit()
    if ok:
        c.execute("INSERT INTO role_log (user_id, role, assigned_by, assigned_at) VALUES (?,?,?,?)",
                  (user_id, role, by_id, datetime.datetime.now().isoformat()))
        conn.commit()
    conn.close()
    return ok

def get_all_staff():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chat_id, username, role FROM users WHERE role IS NOT NULL ORDER BY role")
    rows = c.fetchall(); conn.close()
    return rows



def create_prank_poll(question: str, real_opts: list, mapped_opts: list,
                      mode: str, created_by: int) -> int:
    import json as _j
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO prank_polls
        (question, real_options, mapped_options, mode, created_by, created_at, votes_json)
        VALUES (?,?,?,?,?,?,?)""",
        (question, _j.dumps(real_opts, ensure_ascii=False),
         _j.dumps(mapped_opts, ensure_ascii=False),
         mode, created_by, datetime.datetime.now().isoformat(), "{}"))
    pid = c.lastrowid
    conn.commit(); conn.close()
    return pid

def get_prank_poll(poll_id: int):
    import json as _j
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM prank_polls WHERE id=?", (poll_id,))
    row = c.fetchone(); conn.close()
    if not row:
        return None
    keys = ["id","question","real_options","mapped_options","mode",
            "created_by","created_at","votes_json","is_active","tg_poll_id"]
    d = dict(zip(keys, row))
    d["real_options"] = _j.loads(d["real_options"])
    d["mapped_options"] = _j.loads(d["mapped_options"])
    try:
        d["votes_json"] = _j.loads(d["votes_json"] or "{}")
    except:
        d["votes_json"] = {}
    return d

def record_prank_vote(poll_id: int, user_id: int, chosen_idx: int):
    import json as _j
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT votes_json, mapped_options FROM prank_polls WHERE id=?", (poll_id,))
    row = c.fetchone()
    if not row:
        conn.close(); return None
    votes = _j.loads(row[0] or "{}")
    mapped = _j.loads(row[1])
    str_uid = str(user_id)
    if str_uid in votes:
        conn.close(); return votes[str_uid]["real"]
    real_idx = chosen_idx
    votes[str_uid] = {"chosen": chosen_idx, "real": real_idx}
    c.execute("UPDATE prank_polls SET votes_json=? WHERE id=?", (_j.dumps(votes), poll_id))
    conn.commit(); conn.close()
    return real_idx

def get_prank_poll_stats(poll_id: int):
    import json as _j
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT votes_json, real_options FROM prank_polls WHERE id=?", (poll_id,))
    row = c.fetchone(); conn.close()
    if not row:
        return {}
    votes = _j.loads(row[0] or "{}")
    opts = _j.loads(row[1])
    counts = {i: 0 for i in range(len(opts))}
    for v in votes.values():
        idx = v.get("real", v.get("chosen", 0))
        counts[idx] = counts.get(idx, 0) + 1
    return {opts[i]: counts.get(i, 0) for i in range(len(opts))}

def get_review_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), AVG(rating) FROM reviews")
    row = c.fetchone()
    conn.close()
    total = row[0] or 0
    avg = round(row[1], 2) if row[1] else 0.0
    return total, avg

def add_review(user_id: int, rating: int, text: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO reviews (user_id, rating, text, created_at) VALUES (?,?,?,?)",
              (user_id, rating, text, datetime.datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_reviews(limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT r.user_id, u.username, r.rating, r.text, r.created_at FROM reviews r LEFT JOIN users u ON r.user_id=u.chat_id ORDER BY r.created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close()
    return rows


def get_ref_link(user_id):
    import base64
    token = base64.urlsafe_b64encode(str(user_id).encode()).decode().rstrip("=")
    return "https://t.me/pweper_bot?start=ref_" + token

def decode_ref_token(token):
    import base64
    try:
        padding = 4 - len(token) % 4
        return int(base64.urlsafe_b64decode(token + "=" * padding).decode())
    except:
        return None

def register_referral(referrer_id, referred_id):
    if referrer_id == referred_id:
        return
    suspicious, reason = is_referral_suspicious(referrer_id, referred_id)
    if suspicious:
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO referrals (referrer_id,referred_id,created_at) VALUES (?,?,?)",
                  (referrer_id, referred_id, datetime.datetime.now().isoformat()))
        c.execute("UPDATE users SET referred_by=? WHERE chat_id=? AND (referred_by IS NULL OR referred_by='')",
                  (str(referrer_id), referred_id))
        conn.commit()
    except:
        pass
    conn.close()

def count_paid_referrals(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=? AND paid=1", (user_id,))
    n = c.fetchone()[0]; conn.close()
    return n

def get_buyer_discount(referred_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT referred_by FROM users WHERE chat_id=?", (referred_id,))
    row = c.fetchone(); conn.close()
    if not row or not row[0]:
        return 0
    try:
        referrer_id = int(row[0])
    except:
        return 0
    paid_refs = count_paid_referrals(referrer_id)
    for min_r, disc in REFERRAL_BONUS_TIERS:
        if paid_refs >= min_r:
            return disc
    return 10

def get_l2_reward_pct(referrer_id):
    paid = count_paid_referrals(referrer_id)
    for min_r, pct in L2_REWARD_TIERS:
        if paid >= min_r:
            return pct
    return 1

def mark_referral_paid(referred_id, stars_paid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT referrer_id FROM referrals WHERE referred_id=? AND paid=0", (referred_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None, 0
    referrer_id = row[0]
    reward = max(1, int(stars_paid * REFERRAL_REWARD_PCT / 100))
    c.execute("UPDATE referrals SET paid=1, reward_given=? WHERE referred_id=?",
              (reward, referred_id))
    c.execute("""UPDATE users SET
        ref_balance=CAST(COALESCE(CAST(ref_balance AS INTEGER),0)+? AS TEXT)
        WHERE chat_id=?""", (reward, referrer_id))
    c.execute("SELECT referred_by FROM users WHERE chat_id=?", (referrer_id,))
    l2_row = c.fetchone()
    l2_referrer = None
    l2_reward = 0
    if l2_row and l2_row[0]:
        try:
            l2_id = int(l2_row[0])
            l2_pct = get_l2_reward_pct(l2_id)
            l2_reward = max(1, int(stars_paid * l2_pct / 100))
            c.execute("""UPDATE users SET
                ref_balance=CAST(COALESCE(CAST(ref_balance AS INTEGER),0)+? AS TEXT)
                WHERE chat_id=?""", (l2_reward, l2_id))
            l2_referrer = l2_id
        except:
            pass
    conn.commit()
    conn.close()
    return referrer_id, reward, l2_referrer, l2_reward

def get_ref_stats(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (user_id,))
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=? AND paid=1", (user_id,))
    paid = c.fetchone()[0]
    c.execute("SELECT COALESCE(CAST(ref_balance AS INTEGER),0) FROM users WHERE chat_id=?",
              (user_id,))
    bal_row = c.fetchone()
    balance = bal_row[0] if bal_row else 0
    conn.close()
    return total, paid, balance


# ── Groq rate limit ────────────────────────────────────────────────────
def check_groq_rate(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = __import__('time').time()
    c.execute("SELECT window_start, count FROM groq_rate WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        ws, cnt = row
        if now - ws < 60:
            if cnt >= GROQ_RATE_LIMIT_PER_MIN:
                conn.close()
                return False
            c.execute("UPDATE groq_rate SET count=count+1 WHERE user_id=?", (user_id,))
        else:
            c.execute("UPDATE groq_rate SET window_start=?, count=1 WHERE user_id=?", (now, user_id))
    else:
        c.execute("INSERT INTO groq_rate (user_id, window_start, count) VALUES (?,?,1)", (user_id, now))
    conn.commit(); conn.close()
    return True

# ── Command stats ──────────────────────────────────────────────────────
def log_command(user_id: int, command: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO command_stats (user_id, command, used_at) VALUES (?,?,?)",
              (user_id, command, datetime.datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_command_stats(limit=15):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT command, COUNT(*) as cnt FROM command_stats GROUP BY command ORDER BY cnt DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close()
    return rows

# ── Registration tracking ──────────────────────────────────────────────
def register_user_date(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO registrations (user_id, registered_at) VALUES (?,?)",
              (user_id, datetime.datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_reg_stats(period_hours: int = 24):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    since = (datetime.datetime.now() - datetime.timedelta(hours=period_hours)).isoformat()
    c.execute("SELECT COUNT(*) FROM registrations WHERE registered_at >= ?", (since,))
    count = c.fetchone()[0]
    conn.close()
    return count

def get_reg_chart(period: str = "week"):
    periods = {"hour": (1, "%H:%M", 1), "day": (24, "%H:00", 1),
               "week": (168, "%d.%m", 24), "month": (720, "%d.%m", 24*7), "year": (8760, "%m.%Y", 24*30)}
    hours, fmt, bucket_h = periods.get(period, periods["week"])
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    since = (datetime.datetime.now() - datetime.timedelta(hours=hours)).isoformat()
    c.execute("SELECT registered_at FROM registrations WHERE registered_at >= ? ORDER BY registered_at", (since,))
    rows = c.fetchall(); conn.close()
    buckets = {}
    for (ts,) in rows:
        try:
            dt = datetime.datetime.fromisoformat(ts)
            bucket = dt.strftime(fmt)
            buckets[bucket] = buckets.get(bucket, 0) + 1
        except: pass
    return buckets

# ── Purchase history ───────────────────────────────────────────────────
def log_purchase(user_id: int, stars: int, days: int, plan_label: str,
                 promo_code: str = None, discount_pct: int = 0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO purchases (user_id,stars,days,plan_label,promo_code,discount_pct,created_at) VALUES (?,?,?,?,?,?,?)",
              (user_id, stars, days, plan_label, promo_code, discount_pct, datetime.datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_purchase_history(user_id: int = None, limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("SELECT p.*, u.username FROM purchases p LEFT JOIN users u ON p.user_id=u.chat_id WHERE p.user_id=? ORDER BY p.created_at DESC LIMIT ?", (user_id, limit))
    else:
        c.execute("SELECT p.*, u.username FROM purchases p LEFT JOIN users u ON p.user_id=u.chat_id ORDER BY p.created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close()
    return rows

def get_purchase_stats(period_hours: int = 24):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    since = (datetime.datetime.now() - datetime.timedelta(hours=period_hours)).isoformat()
    c.execute("SELECT COUNT(*), COALESCE(SUM(stars),0) FROM purchases WHERE created_at >= ?", (since,))
    count, total = c.fetchone()
    conn.close()
    return count, total

# ── Support tickets ────────────────────────────────────────────────────
def create_ticket(user_id: int, username: str, is_premium: bool, subject: str, message: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO support_tickets (user_id,username,is_premium,subject,message,created_at) VALUES (?,?,?,?,?,?)",
              (user_id, username, 1 if is_premium else 0, subject, message, datetime.datetime.now().isoformat()))
    ticket_id = c.lastrowid
    conn.commit(); conn.close()
    return ticket_id

def get_open_tickets(premium_first: bool = True):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    order = "is_premium DESC, created_at ASC" if premium_first else "created_at ASC"
    c.execute(f"SELECT id,user_id,username,is_premium,subject,status,created_at FROM support_tickets WHERE status='open' ORDER BY {order}")
    rows = c.fetchall(); conn.close()
    return rows

def get_ticket(ticket_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM support_tickets WHERE id=?", (ticket_id,))
    row = c.fetchone(); conn.close()
    return row

def close_ticket(ticket_id: int, admin_id: int, reply: str = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE support_tickets SET status='closed',closed_at=?,closed_by=?,reply=? WHERE id=?",
              (datetime.datetime.now().isoformat(), admin_id, reply, ticket_id))
    conn.commit(); conn.close()

def get_ticket_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM support_tickets"); total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM support_tickets WHERE status='open'"); open_t = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM support_tickets WHERE is_premium=1 AND status='open'"); prem_open = c.fetchone()[0]
    conn.close()
    return total, open_t, prem_open

# ── Promo: single active per user, auto-expire check ──────────────────
def set_user_active_promo(user_id: int, code: str, expires_at: str = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET active_promo=?, promo_expires=? WHERE chat_id=?",
              (code.upper() if code else None, expires_at, user_id))
    conn.commit(); conn.close()

def get_user_active_promo(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT active_promo, promo_expires FROM users WHERE chat_id=?", (user_id,))
    row = c.fetchone(); conn.close()
    if not row or not row[0]:
        return None
    code, exp = row
    if exp:
        try:
            if datetime.datetime.now() > datetime.datetime.fromisoformat(exp):
                conn2 = sqlite3.connect(DB_PATH)
                c2 = conn2.cursor()
                c2.execute("UPDATE users SET active_promo=NULL, promo_expires=NULL WHERE chat_id=?", (user_id,))
                conn2.commit(); conn2.close()
                return None
        except: pass
    p = get_promo(code)
    if not p:
        conn3 = sqlite3.connect(DB_PATH)
        c3 = conn3.cursor()
        c3.execute("UPDATE users SET active_promo=NULL, promo_expires=NULL WHERE chat_id=?", (user_id,))
        conn3.commit(); conn3.close()
        return None
    return p

# ── Trial subscription ─────────────────────────────────────────────────
def can_use_trial(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT trial_used FROM users WHERE chat_id=?", (user_id,))
    row = c.fetchone(); conn.close()
    return row and row[0] != 'True'

def mark_trial_used(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET trial_used='True' WHERE chat_id=?", (user_id,))
    conn.commit(); conn.close()

# ── Free ref milestone ─────────────────────────────────────────────────
def check_free_ref_milestone(referrer_id: int):
    """Award 1 month Pro when referrer has brought 25 total referrals.
    Stars-based referrals don't count here; milestone fires only once."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (referrer_id,))
    total_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=? AND reward_given=1", (referrer_id,))
    already = c.fetchone()[0]
    awarded = False
    if total_count >= FREE_TRIAL_FREE_REFS and already == 0:
        expiry = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%d.%m.%Y")
        c.execute("UPDATE users SET sub='True', time=? WHERE chat_id=?", (expiry, referrer_id))
        c.execute("UPDATE referrals SET reward_given=1 WHERE referrer_id=?", (referrer_id,))
        awarded = True
    conn.commit(); conn.close()
    return awarded, total_count

# ── Anti-cheat referral ────────────────────────────────────────────────
def is_referral_suspicious(referrer_id: int, referred_id: int) -> tuple:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT registered_at FROM registrations WHERE user_id=?", (referred_id,))
    row = c.fetchone()
    if row:
        try:
            reg = datetime.datetime.fromisoformat(row[0])
            if (datetime.datetime.now() - reg).total_seconds() < 300:
                conn.close()
                return True, "Аккаунт зарегистрирован < 5 минут назад"
        except: pass
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=? AND created_at >= ?",
              (referrer_id, (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()))
    hourly = c.fetchone()[0]
    conn.close()
    if hourly >= 10:
        return True, "Слишком много рефералов за 1 час"
    return False, None

# ── Batch session ──────────────────────────────────────────────────────
def start_batch(user_id: int, command: str, caption: str = ""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO batch_sessions (user_id,command,caption,files,started_at) VALUES (?,?,?,'[]',?)",
              (user_id, command, caption, datetime.datetime.now().isoformat()))
    conn.commit(); conn.close()

def add_batch_file(user_id: int, file_id: str, file_name: str):
    import json as _json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT files FROM batch_sessions WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False
    files = _json.loads(row[0])
    files.append({"file_id": file_id, "file_name": file_name})
    c.execute("UPDATE batch_sessions SET files=? WHERE user_id=?", (_json.dumps(files), user_id))
    conn.commit(); conn.close()
    return True

def get_batch(user_id: int):
    import json as _json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT command, caption, files FROM batch_sessions WHERE user_id=?", (user_id,))
    row = c.fetchone(); conn.close()
    if not row:
        return None
    return {"command": row[0], "caption": row[1], "files": _json.loads(row[2])}

def clear_batch(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM batch_sessions WHERE user_id=?", (user_id,))
    conn.commit(); conn.close()


async def send_invoice_for_plan(chat_id: int, user_id: int, plan: dict):
    payload = f"sub_{plan['stars']}_{plan['days']}_{user_id}_{int(time.time())}"
    save_invoice(payload, user_id, plan['stars'], plan['days'])
    await bot.send_invoice(
        chat_id=chat_id,
        title=f"{plan['emoji']} Premium {plan['label']}",
        description=(
            f"Подписка на {plan['label']}.\n"
            "✅ Без ограничений по размеру файлов\n"
            "✅ Приоритетная очередь\n"
            "✅ Все функции без ограничений"
        ),
        payload=payload,
        currency="XTR",
        prices=[LabeledPrice(label=f"Premium {plan['label']}", amount=plan['stars'])],
    )

def kb_subscription_plans():
    b = InlineKeyboardBuilder()
    for p in SUBSCRIPTION_PLANS:
        b.button(text=f"{p['emoji']} {p['label']} — {p['stars']} ⭐", callback_data=f"buy_{p['stars']}")
    b.button(text="💬 Купить у владельца (@keedboy016)", url="https://t.me/keedboy016")
    b.adjust(1)
    return b.as_markup()

def kb_check_channels(channels: list):
    b = InlineKeyboardBuilder()
    for ch in channels:
        b.button(text=f"📢 {ch}", url=f"https://t.me/{ch.lstrip('@')}")
    b.button(text="✅ Проверить подписку", callback_data="recheck_channels")
    b.adjust(1)
    return b.as_markup()

def kb_admin_main(user_id: int = 0):
    role = get_role(user_id) or "admin"
    lvl = get_role_level(user_id) if user_id else 2
    b = InlineKeyboardBuilder()
    b.button(text="📊 Статистика", callback_data="adm_stats")
    b.button(text="🏆 Топ активности", callback_data="adm_top")
    b.button(text="📈 Графики", callback_data="adm_charts")
    b.button(text="🎫 Тех. поддержка", callback_data="adm_tickets")
    b.button(text="🗑 Очистить work/", callback_data="adm_cleanup")
    if lvl >= 2:
        b.button(text="🚫 Баны", callback_data="adm_bans_list")
        b.button(text="🎁 Выдать подписку", callback_data="adm_givesub_panel")
        b.button(text="📢 Рассылка", callback_data="adm_broadcast")
        b.button(text="📋 Опросы", callback_data="adm_polls_menu")
        b.button(text="🃏 Пранк-опросы", callback_data="adm_prank_menu")
        b.button(text="🎟 Промокоды", callback_data="adm_promos")
        b.button(text="👥 Рефералы", callback_data="adm_ref_stats")
        b.button(text="🛒 История покупок", callback_data="adm_purchases")
        b.button(text="⭐ Отзывы", callback_data="adm_reviews")
    if lvl >= 3:
        b.button(text="📣 Каналы подписки", callback_data="adm_channels")
        b.button(text="👑 Управление ролями", callback_data="adm_roles")
        b.button(text="📋 Лог ролей", callback_data="adm_role_log")
        b.button(text="👮 Активность стаффа", callback_data="adm_staff_stats")
    b.adjust(2)
    return b.as_markup()

def kb_back_admin():
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_main")
    return b.as_markup()

def start_free_text():
    return (
        "👋 <b>Добро пожаловать в " + BOT_NAME + "!</b>\n\n"
        "⚠️ <b>Вы используете бесплатную версию</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "❌ <b>Ограничения без подписки:</b>\n"
        "  • Файлы не более <b>20 МБ</b>\n"
        "  • Задержка <b>2–3 сек</b> перед обработкой\n"
        "  • Ставитесь в очередь <b>за платными</b>\n"
        "  • Обязательна подписка на 3 канала\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ <b>Преимущества Premium:</b>\n"
        "  • Файлы до <b>2 ГБ</b>\n"
        "  • <b>Мгновенная</b> обработка без очереди\n"
        "  • Подписка на каналы <b>не нужна</b>\n"
        "  • Все функции без ограничений\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💎 <b>Тарифы — оплата Telegram Stars ⭐:</b>"
    )

def start_paid_text(expiry: str):
    forever = expiry == "31.12.2099"
    until = "♾️ бессрочно" if forever else f"до <b>{expiry}</b>"
    return (
        f"👋 <b>С возвращением, Premium-пользователь!</b>\n\n"
        f"💎 Подписка активна — {until}\n\n"
        "Все функции без ограничений. Команды — /help"
    )

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        username TEXT,
        sub TEXT DEFAULT 'False',
        admin TEXT DEFAULT 'False',
        time TEXT
    )''')
    for col, defval in [("banned","'False'"),("ban_reason","NULL"),("msg_count","0"),("last_active","NULL"),("role","NULL")]:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT {defval}")
        except sqlite3.OperationalError:
            pass
    c.execute('''CREATE TABLE IF NOT EXISTS required_channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_username TEXT UNIQUE NOT NULL,
        channel_name TEXT
    )''')
    for ch in DEFAULT_CHANNELS:
        c.execute("INSERT OR IGNORE INTO required_channels (channel_username, channel_name) VALUES (?,?)", (ch, ch))
    c.execute('''CREATE TABLE IF NOT EXISTS broadcasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT, sent_at TEXT, sent_by INTEGER, total_sent INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS polls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL, options TEXT NOT NULL,
        created_at TEXT, created_by INTEGER, is_active INTEGER DEFAULT 1
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS prank_polls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        real_options TEXT NOT NULL,
        mapped_options TEXT NOT NULL,
        mode TEXT DEFAULT 'remap',
        created_by INTEGER,
        created_at TEXT,
        votes_json TEXT DEFAULT '{}',
        is_active INTEGER DEFAULT 1,
        tg_poll_id TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS reviews (
        user_id INTEGER PRIMARY KEY,
        rating INTEGER NOT NULL,
        text TEXT,
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS role_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        assigned_by INTEGER,
        assigned_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS antispam (
        user_id INTEGER PRIMARY KEY,
        window_start REAL DEFAULT 0,
        msg_count INTEGER DEFAULT 0,
        blocked_until REAL DEFAULT 0,
        file_window_start REAL DEFAULT 0,
        file_count INTEGER DEFAULT 0,
        file_blocked_until REAL DEFAULT 0
    )''')
    for col3 in ["file_window_start","file_count","file_blocked_until"]:
        try:
            c.execute(f"ALTER TABLE antispam ADD COLUMN {col3} REAL DEFAULT 0")
        except sqlite3.OperationalError:
            pass
    c.execute('''CREATE TABLE IF NOT EXISTS pending_invoices (
        payload TEXT PRIMARY KEY,
        user_id INTEGER, stars INTEGER, days INTEGER, created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS support_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT,
        is_premium INTEGER DEFAULT 0,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        created_at TEXT,
        closed_at TEXT,
        closed_by INTEGER,
        reply TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        stars INTEGER NOT NULL,
        days INTEGER NOT NULL,
        plan_label TEXT,
        promo_code TEXT,
        discount_pct INTEGER DEFAULT 0,
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS command_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        command TEXT NOT NULL,
        used_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS registrations (
        user_id INTEGER PRIMARY KEY,
        registered_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS batch_sessions (
        user_id INTEGER PRIMARY KEY,
        command TEXT NOT NULL,
        caption TEXT,
        files TEXT DEFAULT '[]',
        started_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS groq_rate (
        user_id INTEGER PRIMARY KEY,
        window_start REAL DEFAULT 0,
        count INTEGER DEFAULT 0
    )''')
    for col4, def4 in [("trial_used","'False'"),("active_promo","NULL"),("promo_expires","NULL")]:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col4} TEXT DEFAULT {def4}")
        except:
            pass
    conn.commit()
    conn.close()

initialize_database()

async def save_workbook_to_disk():
    pass

async def update(chat_id, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_date = datetime.datetime.now().date()
    message_to_send = None
    sub = False
    cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    user = cursor.fetchone()
    if user:
        db_chat_id, db_username, db_sub_status, db_admin_status, db_expiration_date_str = user[0], user[1], user[2], user[3], user[4]
        if db_expiration_date_str:
            expiration_date = datetime.datetime.strptime(db_expiration_date_str, "%d.%m.%Y").date()
            if expiration_date <= current_date:
                sub = True
                cursor.execute("UPDATE users SET sub='False', time=NULL WHERE chat_id=?", (chat_id,))
                message_to_send = "⚠️ Ваша подписка закончилась!"
        if db_username != username:
            cursor.execute("UPDATE users SET username=? WHERE chat_id=?", (username, chat_id))
    else:
        cursor.execute("INSERT INTO users (chat_id, username, sub, admin, time) VALUES (?, ?, 'False', 'False', NULL)",
                       (chat_id, username))
        conn2_reg = sqlite3.connect(DB_PATH)
        c2_reg = conn2_reg.cursor()
        c2_reg.execute("INSERT OR IGNORE INTO registrations (user_id, registered_at) VALUES (?,?)",
                       (chat_id, datetime.datetime.now().isoformat()))
        conn2_reg.commit(); conn2_reg.close()
    conn.commit()
    conn.close()
    return sub, message_to_send

def find_user_data_in_sql(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sub, time FROM users WHERE chat_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0] == 'True', result[1]
    return False, None

async def get_user_status_async(user_id):
    return await asyncio.to_thread(find_user_data_in_sql, user_id)

def execute_sql_query(query, params=(), fetchone=False, fetchall=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetchone:
        result = cursor.fetchone()
        conn.close()
        return result
    if fetchall:
        result = cursor.fetchall()
        conn.close()
        return result
    conn.commit()
    conn.close()

def apply_weapon_params(folder: str, PT: int, RAZB: int):
    wj_path = os.path.join(folder, "weapon.json")
    if os.path.exists(wj_path):
        with open(wj_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for weapon in data.get("weapons", []):
            if weapon.get("uniqueName") == "DESERT_EAGLE":
                weapon["ammo"] = PT
                weapon["accuracy"] = RAZB
                break
        with open(wj_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    wo_path = os.path.join(folder, "weapon_overrides.json")
    if os.path.exists(wo_path):
        with open(wo_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "DESERT_EAGLE" in data.get("weapons", {}):
            data["weapons"]["DESERT_EAGLE"]["ammo"] = PT
            data["weapons"]["DESERT_EAGLE"]["accuracy"] = RAZB
        with open(wo_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    wp_path = os.path.join(folder, "weapon_presets.json")
    if os.path.exists(wp_path):
        with open(wp_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "DESERT_EAGLE" in data.get("antiSpreadStaticAim", {}):
            data["antiSpreadStaticAim"]["DESERT_EAGLE"]["accuracy"] = RAZB
        if "DESERT_EAGLE" in data.get("antiReload", {}):
            data["antiReload"]["DESERT_EAGLE"] = PT
        with open(wp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

def build_weapon_zip(tmp_folder: str, zip_path: str):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(tmp_folder):
            zf.write(os.path.join(tmp_folder, fname), fname)

async def send_log(message: types.Message, content_type: str = "текст", extra: str = ""):
    try:
        user = message.from_user
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        uid = user.id
        uname = f"@{user.username}" if user.username else "нет юзернейма"
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        caption = message.caption or ""
        type_icons = {"текст":"💬","фото":"🖼","стикер":"🎭","гифка":"🎞","видео":"🎬","голосовое":"🎤",
                      "аудио":"🎵","файл":"📁","видео-сообщение":"📹","контакт":"👤","геолокация":"📍","опрос":"📊","история":"📖"}
        icon = type_icons.get(content_type, "📋")
        lines = [f"{icon} <b>Лог: {content_type}</b>", f"📅 <code>{now}</code>",
                 f"👤 <b>{full_name}</b>  {uname}", f"🆔 <code>{uid}</code>"]
        if message.chat.type != "private":
            lines.append(f"💬 Чат: <code>{message.chat.id}</code> ({message.chat.title or ''})")
        if extra: lines.append(f"ℹ️ {extra}")
        if caption: lines.append(f"💬 Подпись: {caption}")
        if message.sticker:
            s = message.sticker
            lines.append(f"😄 Emoji: {s.emoji or '—'}  |  Набор: {s.set_name or '—'}")
        elif message.document:
            d = message.document
            size_kb = round(d.file_size / 1024, 1) if d.file_size else "?"
            lines.append(f"📄 Файл: <code>{d.file_name}</code>  ({size_kb} КБ)")
        elif message.photo:
            p = message.photo[-1]
            lines.append(f"📐 Размер: {p.width}×{p.height}  |  {round(p.file_size/1024,1)} КБ")
        elif message.video:
            v = message.video
            lines.append(f"⏱ Длит.: {v.duration}с  |  {v.width}×{v.height}  |  {round(v.file_size/1024/1024,2)} МБ")
        elif message.text:
            preview = message.text[:200] + ("…" if len(message.text) > 200 else "")
            lines.append(f"✉️ {preview}")
        text = "\n".join(lines)
        for chat_id in loging_id:
            await boti.send_message(chat_id, text, parse_mode="HTML")
            try: await message.forward(chat_id)
            except: pass
    except Exception as e:
        logging.warning(f"send_log error: {e}")

def _process_overlay_logic(base_input, overlay_input, mode, alpha_pct):
    base = Image.open(base_input).convert("RGBA")
    overlay = Image.open(overlay_input).convert("RGBA")
    overlay = overlay.resize(base.size, Image.Resampling.LANCZOS)
    if mode == "multiply": effect = ImageChops.multiply(base, overlay)
    elif mode == "screen": effect = ImageChops.screen(ImageChops.screen(base, overlay), overlay)
    elif mode == "overlay": effect = ImageChops.overlay(ImageChops.overlay(base, overlay), overlay)
    elif mode == "add": effect = ImageChops.add(base, overlay)
    elif mode == "darker": effect = ImageChops.darker(base, overlay)
    else: effect = overlay
    base_alpha = base.split()[3]
    user_alpha_level = int(255 * (alpha_pct / 100.0))
    mask = ImageChops.darker(base_alpha, Image.new("L", base.size, user_alpha_level))
    final = Image.composite(effect, base, mask)
    img_byte_arr = io.BytesIO()
    final.convert("RGBA").save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def _process_zip_overlay(zip_path, overlay_img_path, mode, alpha_pct):
    output_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_path, 'r') as archive_in:
        with zipfile.ZipFile(output_zip_buffer, 'a', zipfile.ZIP_DEFLATED) as archive_out:
            for file_info in archive_in.infolist():
                if file_info.is_dir() or file_info.filename.startswith('__MACOSX') or \
                        not file_info.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                with archive_in.open(file_info) as file:
                    try:
                        img_bytes = io.BytesIO(file.read())
                        processed_bytes = _process_overlay_logic(img_bytes, overlay_img_path, mode, alpha_pct)
                        archive_out.writestr(file_info.filename, processed_bytes)
                    except: continue
    output_zip_buffer.seek(0)
    return output_zip_buffer

async def create_palette_image(image_path, file_name, n_colors=10, output_file="palette.png"):
    img = Image.open(image_path).convert('RGB')
    img_small = img.copy()
    img_small.thumbnail((150, 150))
    pixels = np.array(img_small).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b).upper() for r, g, b in colors]
    width, height = 1000, 200
    swatch_width = width // n_colors
    palette_img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(palette_img)
    try: font = ImageFont.truetype("arial.ttf", 16)
    except: font = ImageFont.load_default()
    o = f"Основные цвета изображения {file_name}:\n"
    for i, color in enumerate(colors):
        hex_val = hex_colors[i]
        o = o + f"{i + 1}. {hex_val}\n"
        shape = [i * swatch_width, 0, (i + 1) * swatch_width, height]
        draw.rectangle(shape, fill=tuple(color))
        brightness = (color[0] * 299 + color[1] * 587 + color[1] * 114) / 1000
        text_color = (255, 255, 255) if brightness < 128 else (0, 0, 0)
        draw.text((i * swatch_width + 10, height // 2 - 10), hex_val, fill=text_color, font=font)
    palette_img.save(output_file)
    return o

def random_color():
    h = random.random()
    s = random.uniform(0.5, 0.8)
    l = random.uniform(0.4, 0.7)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255)).upper()

def get_hex_from_description(description):
    desc_clean = description.strip().lower()
    completion = client.chat.completions.create(
        messages=[{"role":"system","content":"Ты эксперт по колористике. Отвечай ТОЛЬКО hex-кодом (например, #FFFFFF), без лишних слов."},
                  {"role":"user","content":f"Цвет: {desc_clean}"}],
        model="llama-3.1-8b-instant", temperature=0.1)
    hex_response = completion.choices[0].message.content.strip()
    match = re.search(r'#[A-Fa-f0-9]{6}', hex_response)
    return match.group(0).upper()

def convert_zip2nonerai(src_file, temp_dir):
    temp_dir1 = Path(temp_dir)
    genrl_orig = "GENERIC.bpc"
    raw_path = temp_dir1 / "raw"
    with zipfile.ZipFile(src_file, 'r') as z:
        z.extractall(raw_path)
    base = next((p.parent for p in raw_path.rglob('NEIZZIR') if p.is_dir()), None)
    if not base: return print("Не найдена папка NEIZZIR")
    build = temp_dir1 / "build"
    ass = build / "Assembly"
    dyn = ass / "dynamic"
    audio_in = ass / "audio"
    audio_out = build / "Audio"
    for p in [dyn, audio_in / "samples", audio_out]: p.mkdir(parents=True, exist_ok=True)
    for fld in ['anim', 'data', 'fonts']:
        if (base / fld).exists(): shutil.move(str(base / fld), str(ass / fld))
    nz = base / 'NEIZZIR'
    for i in range(1, 4):
        s = nz / f"sound_{i}.mp3"
        if s.exists(): shutil.copy2(s, audio_out / f"hit_{i}.mp3")
    gen_temp = temp_dir1 / "gen_work"
    with zipfile.ZipFile(genrl_orig, 'r') as z:
        z.extractall(gen_temp)
    if (nz / 'GENRL').exists():
        shutil.copytree(nz / 'GENRL', gen_temp, dirs_exist_ok=True)
    gen_bpc = audio_in / "samples/GENERIC.bpc"
    with zipfile.ZipFile(gen_bpc, 'w', zipfile.ZIP_STORED) as z:
        for f in gen_temp.rglob('*'):
            if f.is_file(): z.write(f, f.relative_to(gen_temp))
    generate_bpcmeta(str(gen_bpc), audio_in / "GENERIC.bpcmeta")
    for f in nz.iterdir():
        if f.suffix == '.zip' and '.astc' in f.name:
            shutil.move(str(f), str(dyn / "br_tex_nonerai.astc.bpc"))
        elif f.suffix == '.bpc' and 'GENRL' not in f.name:
            shutil.move(str(f), str(dyn / "br_nonerai.bpc"))
    out_name = temp_dir1 / f"{Path(src_file).stem}_converted.nonerai"
    with zipfile.ZipFile(out_name, 'w', zipfile.ZIP_STORED) as z:
        for f in build.rglob('*'):
            if f.is_file(): z.write(f, f.relative_to(build))
    return out_name

def compute_data_offset(zip_path, header_offset):
    with open(zip_path, 'rb') as f:
        f.seek(header_offset + 26)
        n = struct.unpack('<H', f.read(2))[0]
        m = struct.unpack('<H', f.read(2))[0]
        return header_offset + 30 + n + m

def generate_bpcmeta(zip_path_str, output_path_str):
    zip_path = Path(zip_path_str)
    out_path = Path(output_path_str)
    entries = []
    with zipfile.ZipFile(zip_path, 'r') as archive:
        for info in archive.infolist():
            if info.is_dir(): continue
            lower = info.filename.lower()
            if not lower.endswith(('.mp3', '.wav', '.ogg')): continue
            header_offset = getattr(info, 'header_offset', None)
            data_offset = compute_data_offset(str(zip_path), header_offset)
            entries.append({'name': info.filename, 'data_offset': int(data_offset),
                            'comp_size': int(info.compress_size), 'is_mp3': 1 if lower.endswith('.mp3') else 0})
    entries.sort(key=lambda e: e['name'].lower())
    out = bytearray()
    out += struct.pack('<I', len(entries))
    for e in entries:
        name_bytes = e['name'].encode('utf-8')
        out += struct.pack('<I', e['data_offset'])
        out += struct.pack('<I', e['comp_size'])
        out += struct.pack('B', e['is_mp3'])
        out += struct.pack('<H', len(name_bytes))
        out += name_bytes
    out_path.write_bytes(out)

def ror32(x: int, r: int) -> int:
    return ((x >> r) | (x << (32 - r))) & 0xFFFFFFFF

def tea_decrypt_block(data: bytearray, key: list, rounds: int = 8) -> None:
    delta = 0x61C88647
    for offset in range(0, len(data), 8):
        v0, v1 = struct.unpack_from('<II', data, offset)
        sum_val = (-delta * rounds) & 0xFFFFFFFF
        for _ in range(rounds):
            v1 = (v1 - ((v0 + sum_val) ^ (key[3] + (v0 >> 5)) ^ (key[2] + (v0 << 4)))) & 0xFFFFFFFF
            new_sum = (sum_val + v1) & 0xFFFFFFFF
            sum_val = (sum_val + delta) & 0xFFFFFFFF
            v0 = (v0 - (new_sum ^ (key[0] + (v1 << 4)) ^ (key[1] + (v1 >> 5)))) & 0xFFFFFFFF
        struct.pack_into('<II', data, offset, v0, v1)

def patch_dff_header(dff_data: bytearray) -> bytearray:
    if len(dff_data) < 12: return dff_data
    real_size = len(dff_data) - 12
    return dff_data[:4] + struct.pack('<I', real_size) + dff_data[8:]

def clean_dff_data(dff_data: bytearray) -> bytearray:
    end = len(dff_data)
    while end > 0 and dff_data[end - 1] == 0: end -= 1
    return dff_data[:end]

def decrypt_mod_to_dff(mod_bytes: bytes) -> bytes:
    magic, length_val, num_blocks = struct.unpack_from('<III', mod_bytes, 0)
    if magic != 0xAB921033: raise ValueError("invalid .mod file")
    base_key = [0x6ED9EE7A, 0x930C666B, 0x930E166B, 0x4709EE79]
    key = [ror32(k ^ 0x12913AFB, 19) for k in base_key]
    data = bytearray(mod_bytes)
    offset = 28
    for _ in range(num_blocks):
        block = data[offset:offset + 0x800]
        tea_decrypt_block(block, key)
        data[offset:offset + 0x800] = block
        offset += 0x800
    actual_length = min(length_val, len(mod_bytes) - 28)
    dff = bytearray(data[28:28 + actual_length])
    dff = patch_dff_header(dff)
    dff = clean_dff_data(dff)
    return bytes(dff)

async def convert_one(mod_path: str, out_dir: str, log=None):
    name = os.path.splitext(os.path.basename(mod_path))[0]
    os.makedirs(out_dir, exist_ok=True)
    try:
        mod_bytes = open(mod_path, 'rb').read()
        dff_bytes = decrypt_mod_to_dff(mod_bytes)
        out_path = os.path.join(out_dir, name + '.dff')
        with open(out_path, 'wb') as out_f: out_f.write(dff_bytes)
    except Exception as e:
        print(f"[X] error {name}: {e}")

async def convert_timecyc_dat_to_json(input_path, original_filename, temp_dir):
    try:
        with open(input_path, 'r', encoding='utf-8') as f: content = f.read()
        entries = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith(';'): continue
            parts = re.split(r'\s+', line)
            if len(parts) < 48: continue
            entry = {
                "AmbientRGB":[int(parts[0]),int(parts[1]),int(parts[2])],
                "AmbientPhysicalRGB":[int(parts[3]),int(parts[4]),int(parts[5])],
                "DirectionalRGB":[int(parts[6]),int(parts[7]),int(parts[8])],
                "SkyTopRGB":[int(parts[9]),int(parts[10]),int(parts[11])],
                "SkyBottomRGB":[int(parts[12]),int(parts[13]),int(parts[14])],
                "SunCoreRGB":[int(parts[15]),int(parts[16]),int(parts[17])],
                "SunCoronaRGB":[int(parts[18]),int(parts[19]),int(parts[20])],
                "SunSize":float(parts[21]),"SpriteSize":float(parts[22]),"SpriteBrght":float(parts[23]),
                "Shad":int(parts[24]),"LightShad":int(parts[25]),"PoleShad":int(parts[26]),
                "FarClip":float(parts[27]),"FogStart":float(parts[28]),"LightGnd":float(parts[29]),
                "FluffyBottomRGB":[int(parts[30]),int(parts[31]),int(parts[32])],
                "CloudRGB":[int(parts[33]),int(parts[34]),int(parts[35])],
                "WaterRGBA":[int(parts[36]),int(parts[37]),int(parts[38]),int(parts[39])],
                "PostFX1ARGB":[int(parts[40]),int(parts[41]),int(parts[42]),int(parts[43])],
                "PostFX2ARGB":[int(parts[44]),int(parts[45]),int(parts[46]),int(parts[47])],
                "CloudAlpha":int(parts[48]) if len(parts) > 48 else 200
            }
            entries.append(entry)
        json_data = json.dumps(entries, indent=2)
        output_filename = Path(original_filename).stem + '.json'
        output_path = Path(temp_dir) / output_filename
        with open(output_path, 'w', encoding='utf-8') as f: f.write(json_data)
        return output_path
    except Exception as e:
        print(f"Error converting DAT to JSON: {e}")
        return None

async def safe_delete(file_path, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            if file_path.exists():
                if file_path.is_dir(): shutil.rmtree(file_path, ignore_errors=True)
                else: file_path.unlink(missing_ok=True)
                return True
        except: await asyncio.sleep(0.5 * (attempt + 1))
    return False

BTX_QUALITY_MAP = {"fastest":0.0,"fast":10.0,"medium":60.0,"thorough":98.0,"exhaustive":100.0}
BTX_BLOCK_MAP = {"4x4":(4,4),"6x6":(6,6),"8x8":(8,8),"5x5":(5,5),"8x5":(8,5),"8x6":(8,6),"10x10":(10,10),"12x12":(12,12)}
BTX_DEFAULT_BLOCK = (8, 8)
BTX_DEFAULT_QUALITY = 60.0
btx_user_settings: dict = {}

def _btx_internal_format(block_w: int, block_h: int) -> int:
    return {(4,4):0x93B0,(5,5):0x93B2,(6,6):0x93B4,(8,5):0x93B5,(8,6):0x93B6,(8,8):0x93B7,(10,10):0x93BB,(12,12):0x93BD}[(block_w,block_h)]

def _compress_to_btx_bytes(img, block_w=8, block_h=8, quality=60.0):
    from astc_encoder import ASTCConfig, ASTCContext, ASTCImage, ASTCProfile, ASTCSwizzle, ASTCType
    img = img.convert("RGBA")
    w, h = img.size
    cfg = ASTCConfig(ASTCProfile.LDR, block_w, block_h, 1, quality)
    ctx = ASTCContext(cfg)
    aimg = ASTCImage(ASTCType.U8, w, h, data=img.tobytes())
    comp = ctx.compress(aimg, ASTCSwizzle.from_str("RGBA"))
    ktx_id = bytes([0xAB,0x4B,0x54,0x58,0x20,0x31,0x31,0xBB,0x0D,0x0A,0x1A,0x0A])
    hdr = struct.pack("<13I",0x04030201,0,1,0,_btx_internal_format(block_w,block_h),0x1908,w,h,0,0,1,1,0)
    return b'\x02\x00\x00\x00' + ktx_id + hdr + struct.pack("<I", len(comp)) + comp

def _decompress_from_btx_bytes(data):
    from astc_encoder import ASTCConfig, ASTCContext, ASTCImage, ASTCProfile, ASTCSwizzle, ASTCType
    FORMAT_MAP = {v: k for k, v in {(4,4):0x93B0,(5,5):0x93B2,(6,6):0x93B4,(8,5):0x93B5,(8,6):0x93B6,(8,8):0x93B7,(10,10):0x93BB,(12,12):0x93BD}.items()}
    offset = 4 + 12
    hdr = struct.unpack_from("<13I", data, offset)
    gl_fmt, w, h = hdr[4], hdr[6], hdr[7]
    block_w, block_h = FORMAT_MAP[gl_fmt]
    comp = data[offset + 52 + 4:]
    cfg = ASTCConfig(ASTCProfile.LDR, block_w, block_h, 1, 60.0)
    ctx = ASTCContext(cfg)
    aimg = ASTCImage(ASTCType.U8, w, h)
    ctx.decompress(comp, aimg, ASTCSwizzle.from_str("RGBA"))
    return Image.frombytes("RGBA", (w, h), bytes(aimg.data))

async def convert_png_to_btx(input_path, original_filename, temp_dir, block_w=8, block_h=8, quality=60.0):
    try:
        loop = asyncio.get_event_loop()
        img = await loop.run_in_executor(None, Image.open, str(input_path))
        btx = await loop.run_in_executor(None, _compress_to_btx_bytes, img, block_w, block_h, quality)
        out_name = Path(temp_dir) / (Path(original_filename).stem + ".btx")
        async with aiofiles.open(str(out_name), "wb") as f: await f.write(btx)
        return out_name
    except Exception as e:
        logging.error(f"convert_png_to_btx: {e}")
        return None

async def convert_btx_to_png(input_path, original_filename, temp_dir):
    try:
        async with aiofiles.open(str(input_path), "rb") as f: data = await f.read()
        loop = asyncio.get_event_loop()
        img = await loop.run_in_executor(None, _decompress_from_btx_bytes, data)
        out_name = Path(temp_dir) / (Path(original_filename).stem + ".png")
        await loop.run_in_executor(None, img.save, str(out_name), "PNG")
        return out_name
    except Exception as e:
        logging.error(f"convert_btx_to_png: {e}")
        return None

async def convert_png_to_btx_pvr(input_path, temp_ktx, block_w=8, block_h=8, quality=60.0):
    try:
        loop = asyncio.get_event_loop()
        img = await loop.run_in_executor(None, Image.open, str(input_path))
        btx = await loop.run_in_executor(None, _compress_to_btx_bytes, img, block_w, block_h, quality)
        async with aiofiles.open(str(temp_ktx), "wb") as f: await f.write(btx)
        return True
    except Exception as e:
        logging.error(f"convert_png_to_btx_pvr: {e}")
        return False

async def convert_btx_to_png_pvr(temp_ktx, output_path):
    try:
        async with aiofiles.open(str(temp_ktx), "rb") as f: data = await f.read()
        loop = asyncio.get_event_loop()
        img = await loop.run_in_executor(None, _decompress_from_btx_bytes, data)
        await loop.run_in_executor(None, img.save, str(output_path), "PNG")
        return True
    except Exception as e:
        logging.error(f"convert_btx_to_png_pvr: {e}")
        return False

def read_file_bytes(file_path):
    with open(file_path, 'rb') as f: return bytearray(f.read())

def write_bytes_to_file(file_path, data):
    with open(file_path, 'wb') as f: f.write(data)

def detect_key_pattern(encrypted_data):
    signatures = {'ZIP': b'PK', 'PNG': b'\x89PNG', 'JPEG': b'\xFF\xD8\xFF', 'GIF': b'GIF', 'PDF': b'%PDF'}
    for key_len in [20, 16, 32, 8, 4]:
        test_key = bytearray()
        for i in range(key_len):
            for sig_type, sig_bytes in signatures.items():
                if i < len(sig_bytes): test_key.append(encrypted_data[i] ^ sig_bytes[i])
        if test_key:
            test_decrypted = bytes([encrypted_data[i] ^ test_key[i % len(test_key)] for i in range(min(100, len(encrypted_data)))])
            for sig_type, sig_bytes in signatures.items():
                if test_decrypted.startswith(sig_bytes): return test_key
    return bytes.fromhex('31 63 4b 31 61 35 55 46 32 74 55 38 2a 47 32 6c 57 23 26 25'.replace(' ',''))

async def process_bpc_file(file_name, message: types.Message, r, temp_dir):
    try:
        file_path = os.path.join(temp_dir, file_name)
        decrypted_file = os.path.join(temp_dir, "decrypted_file")
        encrypted = read_file_bytes(file_path)
        xor_key = detect_key_pattern(encrypted)
        decrypted = bytearray(encrypted[i] ^ xor_key[i % len(xor_key)] for i in range(len(encrypted)))
        write_bytes_to_file(decrypted_file, decrypted)
        if zipfile.is_zipfile(decrypted_file):
            content_dir = os.path.join(temp_dir, "content")
            os.makedirs(content_dir, exist_ok=True)
            with zipfile.ZipFile(decrypted_file, 'r') as zip_ref: zip_ref.extractall(content_dir)
            zip_filename = f"{r}_common.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(content_dir):
                    for file in files:
                        file_path2 = os.path.join(root, file)
                        zipf.write(file_path2, os.path.relpath(file_path2, content_dir))
            await t_client.send_file(message.chat.id, zip_path, caption='<b>⚡️Ваш файл готов!</b>', parse_mode="HTML", force_document=True)
        else:
            await t_client.send_file(message.chat.id, decrypted_file, caption='<b>⚡️Ваш файл готов!</b>', parse_mode="HTML", force_document=True)
    finally:
        if os.path.exists(temp_dir): rmtree(temp_dir, ignore_errors=True)

async def process_zip_file(file_name, message: types.Message, r, temp_dir):
    file_path = os.path.join(temp_dir, file_name)
    encrypted_file = os.path.join(temp_dir, f"{r}_common.bpc")
    original_data = read_file_bytes(file_path)
    xor_key = bytes.fromhex('316 34b3161355546327455382a47326c572323 25'.replace(' ',''))
    encrypted = bytearray(original_data[i] ^ xor_key[i % len(xor_key)] for i in range(len(original_data)))
    write_bytes_to_file(encrypted_file, encrypted)
    await t_client.send_file(message.chat.id, encrypted_file, caption='<b>⚡️Ваш файл готов!</b>', parse_mode="HTML", force_document=True)

def rgb_to_hex(rgb):
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

def process_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f: content = f.read()
    except FileNotFoundError:
        return "Файл не найден"
    colors_to_find = ["SkyBottomRGB", "SkyTopRGB", "CloudRGB", "SunCoreRGB"]
    results = []
    for key in colors_to_find:
        pattern = rf'"{key}"\s*:\s*\[\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*\]'
        match = re.search(pattern, content)
        if match: results.append(f"{key}: {rgb_to_hex(match.groups())}")
        else: results.append(f"{key}: Не найден или кривой формат")
    return "\n".join(results)

def search_in_skins(query: str):
    results = []
    try:
        with open('Editing/skins.txt', 'r', encoding='utf-8') as file:
            current_id = None
            current_name = None
            for line in file:
                line = line.strip()
                if line.startswith("ID - "): current_id = line[5:]
                elif line.startswith("NAME - "):
                    current_name = line[7:]
                    if current_id and current_name:
                        if query == current_id: return [(current_id, current_name)]
                        clean_query = query.lower().replace('.mod', '')
                        mod_name = current_name.lower().replace('.mod', '')
                        if clean_query in mod_name: results.append((current_id, current_name))
                        current_id = None; current_name = None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    return results

async def filerpoisk(id_xyina: str, name_xyina: str, message):
    mod_name = name_xyina.replace('.mod', '').lower()
    dff_path = os.path.join('Editing', 'mod', f"{mod_name}.mod")
    dff_file = FSInputFile(dff_path) if os.path.exists(dff_path) else None
    zip_path = os.path.join('Editing', 'texture', f"texture_{mod_name}.zip")
    zip_file = FSInputFile(zip_path) if os.path.exists(zip_path) else None
    media_group = []
    text_parts = []
    if dff_file:
        media_group.append(InputMediaDocument(media=dff_file))
        text_parts.append(f"{mod_name}.mod")
    if zip_file:
        media_group.append(InputMediaDocument(media=zip_file, caption=f"ID - {id_xyina}\nNAME - {name_xyina}"))
        text_parts.append(f"texture_{mod_name}.zip")
    if media_group: await message.answer_media_group(media=media_group)
    return text_parts

def assemble_image_from_zip_bytes(zip_bytes, name):
    scale_factor = 1.275
    positions_map = {'hud_back.png':(450,240),'hud_up.png':(40,150),'hud_center.png':(40,290),
                     'hud_down.png':(40,490),'hud_menu.png':(40,770),'hud_donat_store.png':(520,770)}
    assembled_img = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0))
    with zipfile.ZipFile(zip_bytes, 'r') as zip_file:
        for filename in zip_file.namelist():
            if filename in positions_map:
                pos = positions_map[filename]
                try:
                    with zip_file.open(filename) as img_file:
                        img_bytes = img_file.read()
                        img_part = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
                        new_size = (int(img_part.width * scale_factor), int(img_part.height * scale_factor))
                        img_part = img_part.resize(new_size, Image.Resampling.LANCZOS)
                        assembled_img.paste(img_part, pos, img_part)
                except: pass
    assembled_img.save(name, format='PNG')

def process_image_sync(file):
    img = Image.open(file).convert("RGBA")
    data = np.array(img)
    alpha = data[:, :, 3]
    kernel_disk = disk(2)
    binary = (alpha > 0).astype(np.uint8) * 255
    try:
        thresh_val = threshold_otsu(alpha)
        binary = (alpha > thresh_val).astype(np.uint8) * 255
    except ValueError:
        binary = (alpha > 0).astype(np.uint8) * 255
    binary_bool = binary.astype(bool)
    closed_bool = closing(binary_bool, kernel_disk)
    opened_bool = opening(closed_bool, kernel_disk)
    labels = label(opened_bool, connectivity=2)
    regions = regionprops(labels)
    objects = []
    for props in regions:
        if props.area < 500: continue
        y1, x1, y2, x2 = props.bbox
        x1_pad = max(0, x1 - 10); y1_pad = max(0, y1 - 10)
        x2_pad = min(data.shape[1], x2 + 10); y2_pad = min(data.shape[0], y2 + 10)
        object_img_data = data[y1_pad:y2_pad, x1_pad:x2_pad, :3]
        relative_labels_slice = labels[y1_pad:y2_pad, x1_pad:x2_pad]
        object_mask_bool = (relative_labels_slice == props.label)
        object_mask_closed_bool = closing(object_mask_bool, kernel_disk)
        object_mask = object_mask_closed_bool.astype(np.uint8) * 255
        object_img = np.zeros((y2_pad - y1_pad, x2_pad - x1_pad, 4), dtype=np.uint8)
        object_img[:, :, :3] = object_img_data
        object_img[:, :, 3] = object_mask
        objects.append((props.area, object_img))
    objects.sort(reverse=True, key=lambda x: x[0])
    if len(objects) == 6: prefixes = ['hud_back', 'hud_down', 'hud_up', 'hud_center', 'hud_menu', 'hud_donat_store']
    elif len(objects) == 5: prefixes = ['hud_down', 'hud_up', 'hud_center', 'hud_menu', 'hud_donat_store']
    else: prefixes = [f'hud_part_{i + 1}' for i in range(len(objects))]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, (_, img_data) in enumerate(objects):
            img_pil = Image.fromarray(img_data, 'RGBA')
            with io.BytesIO() as img_buffer:
                img_pil.save(img_buffer, format='PNG')
                filename = f"{prefixes[i]}.png" if i < len(prefixes) else f"hud_extra_{i + 1}.png"
                zip_file.writestr(filename, img_buffer.getvalue())
    zip_buffer.seek(0)
    return zip_buffer, len(objects)

def create_and_zip_files(base_src_path, output_dir, zip_name, file_format, name, file_SUFFIXES):
    zip_path = os.path.join(output_dir, f"{zip_name}_{name}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for suffix in file_SUFFIXES:
            archive.write(base_src_path, f"{suffix}.{file_format}")
    if os.path.getsize(zip_path) >= MAX_FILE_SIZE:
        os.remove(zip_path)
        return False, None
    return True, zip_path

def recolor_image_optimized_sync(image_path_or_bytes, hex_color, alpha=1.0):
    if not (0.0 <= alpha <= 1.0): alpha = 1.0
    try: new_color_np = np.array(mcolors.to_rgb(hex_color), dtype=np.float32)
    except ValueError: new_color_np = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    if isinstance(image_path_or_bytes, bytes): img = Image.open(io.BytesIO(image_path_or_bytes))
    else: img = Image.open(image_path_or_bytes)
    if img.mode != 'RGBA': img = img.convert('RGBA')
    img_np = np.array(img, dtype=np.float32) / 255.0
    rgb_channels = img_np[:, :, :3]
    original_alpha_channel = img_np[:, :, 3:4]
    luminosity = np.dot(rgb_channels, [0.21, 0.72, 0.07])[:, :, np.newaxis]
    target_color_applied = luminosity * new_color_np
    blended_rgb = rgb_channels * (1.0 - alpha) + target_color_applied * alpha
    blended_img_np = (blended_rgb * 255.0).clip(0, 255).astype(np.uint8)
    final_img_np = np.concatenate([blended_img_np, (original_alpha_channel * 255).astype(np.uint8)], axis=2)
    new_img = Image.fromarray(final_img_np, 'RGBA')
    buffer = io.BytesIO()
    new_img.save(buffer, format="PNG")
    return buffer.getvalue()

def sync_process_file_task_optimized(file_path, color_hex, alpha):
    image_bytes = recolor_image_optimized_sync(str(file_path), color_hex, alpha)
    return image_bytes, file_path.name

async def color(color_hex, src_zip_path, original_zip_name: str, alpha=1.0):
    r = generate_random_string(length)
    work_dir = Path(f'work/work_HUD/{r}')
    await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
    await asyncio.to_thread(zipfile.ZipFile(src_zip_path, 'r').extractall, work_dir)
    files_to_process = [f for f in work_dir.glob('*') if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    tasks = [asyncio.to_thread(sync_process_file_task_optimized, f, color_hex, alpha) for f in files_to_process]
    processed_files_info = await asyncio.gather(*tasks)
    output_zip_dir = Path(f'work/work_HUD/{r}')
    await asyncio.to_thread(os.makedirs, output_zip_dir, exist_ok=True)
    output_zip_path = output_zip_dir / f'{original_zip_name}_{r}.zip'
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        for image_bytes, arcname in processed_files_info: f.writestr(arcname, image_bytes)
    return output_zip_dir, output_zip_path

def _process_image_bytes(image_bytes, color_hex, alpha):
    if not (0.0 <= alpha <= 1.0): alpha = 1.0
    try: new_color_np = np.array(mcolors.to_rgb(color_hex), dtype=np.float32)
    except ValueError: new_color_np = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    try:
        img = Image.open(io.BytesIO(image_bytes) if isinstance(image_bytes, bytes) else image_bytes)
        if img.mode != 'RGBA': img = img.convert('RGBA')
        img_np = np.array(img, dtype=np.float32) / 255.0
        rgb_channels = img_np[:, :, :3]
        original_alpha_channel = img_np[:, :, 3:4]
        luminosity = np.dot(rgb_channels, [0.21, 0.72, 0.07])[:, :, np.newaxis]
        target_color_applied = luminosity * new_color_np
        blended_rgb = rgb_channels * (1.0 - alpha) + target_color_applied * alpha
        blended_img_np = (blended_rgb * 255.0).clip(0, 255).astype(np.uint8)
        final_img_np = np.concatenate([blended_img_np, (original_alpha_channel * 255).astype(np.uint8)], axis=2)
        new_img = Image.fromarray(final_img_np, 'RGBA')
        buffer = io.BytesIO()
        new_img.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return None

async def color_optimized(color_hex, src_zip_path, original_zip_name: str, alpha=1.0):
    r = generate_random_string(4)
    files_to_process = []
    with zipfile.ZipFile(src_zip_path, 'r') as src_zip:
        for zip_info in src_zip.infolist():
            if not zip_info.is_dir() and zip_info.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                files_to_process.append((zip_info.filename, src_zip.read(zip_info.filename)))
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor, _process_image_bytes, img, color_hex, alpha) for filename, img in files_to_process]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    processed_files_info = [(res, fn) for (fn, _), res in zip(files_to_process, results) if not isinstance(res, Exception) and res is not None]
    output_zip_dir = Path(f'work/work_HUD/{r}')
    await asyncio.to_thread(os.makedirs, output_zip_dir, exist_ok=True)
    output_zip_path = output_zip_dir / f'{original_zip_name}_{r}.zip'
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        for image_bytes, arcname in processed_files_info: f.writestr(arcname, image_bytes)
    return output_zip_dir, output_zip_path

def is_float(s):
    try: float(s); return True
    except ValueError: return False

async def setup_work_dirs():
    work_dirs = ['work/', 'work/work_MAP/', 'work/work_BILD/', 'work/work_BLOOD/',
                 'work/work_LOGO/', 'work/work_TREE/', 'work/work_COLOR/',
                 'work/work_BTX/', 'work/work_TXD/', 'work/work_BPC/',
                 'work/work_HUD/', 'work/work_ANI/', 'work/work_COMPRESS', 'work/work_COL', 'work/work_MOD',
                 'work/work_Z2N', "work/work_OVERLAY", "work/work_weapons"]
    for d in work_dirs: os.makedirs(d, exist_ok=True)

def generate_random_string(length=4):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def parse_caption(caption):
    parts = caption.split()
    if '/color' not in parts: return None, None, None
    try:
        hex_color = parts[1]
        if not hex_color.startswith('#'): hex_color = '#' + hex_color
    except IndexError: return None, None, None
    alpha = 1.0
    try:
        if len(parts) > 2: alpha = float(parts[2])
    except ValueError: pass
    return hex_color, alpha

def parse_text(text):
    parts = text.split()
    if '/color' not in parts: return None, None
    try:
        hex_color = parts[1]
        if not hex_color.startswith('#'): hex_color = '#' + hex_color
    except IndexError: return None, None
    alpha = 1.0
    try:
        if len(parts) > 2: alpha = float(parts[2])
    except ValueError: pass
    return hex_color, alpha

def parse_quality(text):
    parts = text.split()
    if '/quality' not in parts: return None
    try: return parts[1]
    except IndexError: return None

def parse_filter(caption):
    parts = caption.split()
    if '/filters' not in parts: return None, None
    try: filter_name = parts[1]
    except IndexError: return None, None
    colvo = 50
    try:
        if len(parts) > 2: colvo = int(parts[2])
    except ValueError: pass
    return filter_name, colvo

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6: raise ValueError("Неверный формат шестнадцатеричного цвета")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def _apply_recolor_to_bytes(image_bytes, target_hex_color, replacement_hex_color, tolerance=10):
    try:
        target_rgb_tuple = hex_to_rgb(target_hex_color)
        img = Image.open(image_bytes if isinstance(image_bytes, io.BytesIO) else io.BytesIO(image_bytes) if isinstance(image_bytes, bytes) else image_bytes)
        if img.mode != 'RGBA': img = img.convert('RGBA')
        img_np = np.array(img, dtype=np.uint8)
        rgb_channels = img_np[:, :, :3]
        alpha_channel = img_np[:, :, 3]
        target_np = np.array(target_rgb_tuple, dtype=np.uint8)
        color_match_mask = np.all(np.abs(rgb_channels.astype(int) - target_np.astype(int)) <= tolerance, axis=-1)
        if str(replacement_hex_color).lower() == 'none':
            alpha_channel[color_match_mask] = 0
        else:
            replacement_rgb_tuple = hex_to_rgb(replacement_hex_color)
            rgb_channels[color_match_mask] = replacement_rgb_tuple
            alpha_channel[color_match_mask] = 255
        final_img_np = np.dstack((rgb_channels, alpha_channel))
        new_img = Image.fromarray(final_img_np, 'RGBA')
        buffer = io.BytesIO()
        new_img.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception as e:
        logging.error(f"Ошибка обработки изображения: {e}")
        return None

def parse_recolor_command(caption):
    parts = caption.split()
    if len(parts) < 3 or len(parts) > 4: return None
    target_hex = parts[1]
    replacement_hex = parts[2]
    tolerance = 10
    if len(parts) == 4:
        try:
            tolerance = int(parts[3])
            if not (0 <= tolerance <= 255): return None
        except ValueError: return None
    if not (target_hex.startswith('#') and len(target_hex) == 7): return None
    return target_hex, replacement_hex, tolerance

def process_aim_image_optimized(image_bytes):
    img = Image.open(image_bytes)
    if img.mode != 'RGBA': img = img.convert('RGBA')
    new_img = Image.new("RGBA", (img.width * 2, img.height * 2))
    new_img.paste(img, (0, 0))
    new_img.paste(img.rotate(90), (0, img.height))
    new_img.paste(img.rotate(180), (img.width, img.height))
    new_img.paste(img.rotate(270), (img.width, 0))
    buffer = io.BytesIO()
    new_img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()

async def recolor_zip_optimized(target_hex, replacement_hex, tolerance, src_zip_path):
    files_to_process = []
    with zipfile.ZipFile(src_zip_path, 'r') as src_zip:
        for zip_info in src_zip.infolist():
            if not zip_info.is_dir() and zip_info.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                files_to_process.append((zip_info.filename, src_zip.read(zip_info.filename)))
    loop = asyncio.get_running_loop()
    processed_files_info = []
    with ThreadPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor, _apply_recolor_to_bytes, image_bytes, target_hex, replacement_hex, tolerance) for filename, image_bytes in files_to_process]
        results = await asyncio.gather(*tasks)
        for i, result_bytes in enumerate(results):
            if result_bytes is not None: processed_files_info.append((result_bytes, files_to_process[i][0]))
    buffer_out = io.BytesIO()
    with zipfile.ZipFile(buffer_out, 'w', compression=zipfile.ZIP_DEFLATED) as f_out:
        for image_bytes_result, arcname in processed_files_info: f_out.writestr(arcname, image_bytes_result)
    buffer_out.seek(0)
    return buffer_out.getvalue()

def quality_func(image_bytes, level):
    level = int(level)
    image = Image.open(image_bytes)
    if image.mode != 'RGBA': image = image.convert('RGBA')
    for _ in range(max(1, int(level / 10))): image = image.filter(ImageFilter.MedianFilter(size=3))
    new_size = (int(image.width * 1.5), int(image.height * 1.5))
    image = image.resize(new_size, Image.LANCZOS)
    for _ in range(2): image = image.filter(ImageFilter.SMOOTH)
    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150 + level, threshold=3))
    image = ImageEnhance.Contrast(image).enhance(1.1 + (level * 0.005))
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='PNG', optimize=True)
    return output_buffer.getvalue()

async def quality_zip(level, src_zip_path):
    files_to_process = []
    with zipfile.ZipFile(src_zip_path, 'r') as src_zip:
        for zip_info in src_zip.infolist():
            if not zip_info.is_dir() and zip_info.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                files_to_process.append((zip_info.filename, src_zip.read(zip_info.filename)))
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor, quality_func, image_bytes, level) for filename, image_bytes in files_to_process]
        results = await asyncio.gather(*tasks)
    buffer_out = io.BytesIO()
    with zipfile.ZipFile(buffer_out, 'w', compression=zipfile.ZIP_DEFLATED) as f_out:
        for i, result_bytes in enumerate(results):
            if result_bytes is not None: f_out.writestr(files_to_process[i][0], result_bytes)
    buffer_out.seek(0)
    return buffer_out.getvalue()

def parse_caption_for_compression(caption):
    try:
        parts = caption.split()
        size_str = next((p for p in parts if 'x' in p), None)
        if not size_str: return None, None
        width, height = map(int, size_str.split('x'))
        return width, height
    except ValueError: return None, None

def _compress_image_bytes_sync(image_bytes, target_size, original_format):
    try:
        with Image.open(image_bytes) as img:
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()
            if original_format.lower() == 'png' and img.mode in ('RGBA', 'P'):
                img.save(output_buffer, format='PNG', optimize=True)
                return output_buffer.getvalue(), 'png'
            else:
                if img.mode != 'RGB': img = img.convert('RGB')
                img.save(output_buffer, format='JPEG', optimize=True, quality=85)
                return output_buffer.getvalue(), 'jpg'
    except Exception as e:
        print(f"Error during image processing: {e}")
        return b"", ""

def _process_zip_sync(download_path, output_zip_path, target_size):
    with open(download_path, 'rb') as f: input_zip_bytes = f.read()
    output_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(input_zip_bytes), 'r') as input_zip:
        with zipfile.ZipFile(output_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as output_zip:
            for filename in input_zip.namelist():
                file_format = filename.split('.')[-1].lower()
                if file_format in ("png", "jpg", "jpeg"):
                    try:
                        image_bytes = input_zip.read(filename)
                        processed_bytes, new_format = _compress_image_bytes_sync(image_bytes, target_size, file_format)
                        output_zip.writestr(Path(filename).stem + f'.{new_format}', processed_bytes)
                    except: output_zip.writestr(filename, input_zip.read(filename))
                else: output_zip.writestr(filename, input_zip.read(filename))
    with open(output_zip_path, 'wb') as f: f.write(output_zip_buffer.getvalue())

def apply_filter_on_bytes_optimized(image_bytes, filter_name, colvo=50):
    img_pil = Image.open(image_bytes if isinstance(image_bytes, io.BytesIO) else io.BytesIO(image_bytes) if isinstance(image_bytes, bytes) else image_bytes)
    if img_pil.mode != 'RGBA': img_pil = img_pil.convert('RGBA')
    img_arr = np.array(img_pil)
    rgb_channels = img_arr[:, :, :3]
    alpha_channel = img_arr[:, :, 3]
    filter_name = filter_name.lower()
    enhancement_factor = 1.5
    if filter_name == 'red':
        rgb_channels[:, :, 0] = np.clip(rgb_channels[:, :, 0].astype(np.uint16) * enhancement_factor, 0, 255).astype(np.uint8)
        filtered_rgb = rgb_channels
    elif filter_name == 'green':
        rgb_channels[:, :, 1] = np.clip(rgb_channels[:, :, 1].astype(np.uint16) * enhancement_factor, 0, 255).astype(np.uint8)
        filtered_rgb = rgb_channels
    elif filter_name == 'blue':
        rgb_channels[:, :, 2] = np.clip(rgb_channels[:, :, 2].astype(np.uint16) * enhancement_factor, 0, 255).astype(np.uint8)
        filtered_rgb = rgb_channels
    elif filter_name == 'grayscale':
        grayscale_2d = np.dot(rgb_channels[..., :3], [0.2989, 0.5870, 0.1140])
        filtered_rgb = np.clip(np.repeat(grayscale_2d[:, :, np.newaxis], 3, axis=2), 0, 255).astype(np.uint8)
    elif filter_name == 'negate': filtered_rgb = 255 - rgb_channels
    elif filter_name == 'sepia':
        sepia_matrix = np.array([[0.272,0.534,0.131],[0.349,0.686,0.168],[0.393,0.769,0.189]]).T
        filtered_rgb = np.clip(np.dot(rgb_channels.astype(np.float32)/255.0, sepia_matrix.T)*255.0, 0, 255).astype(np.uint8)
    elif filter_name == 'solarize':
        filtered_rgb = rgb_channels.copy()
        filtered_rgb[rgb_channels > 128] = 255 - filtered_rgb[rgb_channels > 128]
    elif filter_name == 'light': filtered_rgb = np.clip(rgb_channels.astype(np.int16) + colvo, 0, 255).astype(np.uint8)
    elif filter_name == 'saturation':
        from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
        hsv = rgb_to_hsv(rgb_channels / 255.0)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1 + colvo / 100.0), 0, 1)
        filtered_rgb = (hsv_to_rgb(hsv) * 255).astype(np.uint8)
    elif filter_name == 'contrast':
        factor = (259 * (colvo + 255)) / (255 * (259 - colvo))
        filtered_rgb = np.clip(factor * (rgb_channels.astype(np.float32) - 128) + 128, 0, 255).astype(np.uint8)
    elif filter_name == 'clarity':
        from scipy.ndimage import gaussian_filter
        blurred = gaussian_filter(rgb_channels.astype(np.float32), sigma=1, axes=(0, 1))
        filtered_rgb = np.clip(rgb_channels + (rgb_channels - blurred) * (colvo / 50.0), 0, 255).astype(np.uint8)
    else: raise ValueError(f"Неизвестный фильтр: '{filter_name}'")
    final_img_pil = Image.fromarray(np.dstack([filtered_rgb, alpha_channel]), 'RGBA')
    with io.BytesIO() as buf:
        final_img_pil.save(buf, format='PNG')
        return buf.getvalue()

async def filter_zip(filter_name, src_zip_path, original_zip_name):
    r = generate_random_string(length)
    work_dir = Path(f'work/work_filter_{r}')
    await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
    await asyncio.to_thread(zipfile.ZipFile(src_zip_path, 'r').extractall, work_dir)
    files_to_process = [f for f in work_dir.glob('*') if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    def sync_task(file_path, fn):
        with open(file_path, 'rb') as f: image_bytes = f.read()
        return apply_filter_on_bytes_optimized(image_bytes, fn), file_path.name
    tasks = [asyncio.to_thread(sync_task, f, filter_name) for f in files_to_process]
    processed_files_info = await asyncio.gather(*tasks)
    output_zip_dir = Path(f'work/output_zips/')
    await asyncio.to_thread(os.makedirs, output_zip_dir, exist_ok=True)
    output_zip_path = output_zip_dir / f'{original_zip_name}_filtered_{filter_name}_{r}.zip'
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        for image_bytes, arcname in processed_files_info: f.writestr(arcname, image_bytes)
    await asyncio.to_thread(shutil.rmtree, work_dir)
    return output_zip_path

async def colorcyc(r, b, g):
    with open('BASEcolorcycle.dat', 'r') as f: template_data = f.read()
    final_data = template_data.replace("r", r).replace("g", g).replace("b", b)
    rand_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    grn1 = f"{rand_string}_colorcycle.dat"
    with open(grn1, 'w') as f: f.write(final_data)
    return grn1

async def timecyc(j):
    rand_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    output_file_path = f"{rand_string}_timecyc.json"
    with open("main.json", "r", encoding='utf-8') as f: timecyc_json_string = f.read()
    replacements = [
        ('"SkyBottomRGB":[SBR016]', f'"SkyBottomRGB":{str(list(ImageColor.getrgb(j[1]))).replace(" ","")}'),
        ('"SkyTopRGB":[STR016]', f'"SkyTopRGB":{str(list(ImageColor.getrgb(j[2]))).replace(" ","")}'),
        ('"CloudRGB":[CLR016]', f'"CloudRGB":{str(list(ImageColor.getrgb(j[3]))).replace(" ","")}'),
        ('"SunCoreRGB":[SCR016]', f'"SunCoreRGB":{str(list(ImageColor.getrgb(j[4]))).replace(" ","")}'),
    ]
    for old_text, new_text in replacements: timecyc_json_string = timecyc_json_string.replace(old_text, new_text)
    with open(output_file_path, "w", encoding='utf-8') as f: f.write(timecyc_json_string)
    return output_file_path

def _sync_aitimecyc(description: str) -> dict:
    prompt = f"""Ты эксперт по настройке атмосферы в играх GTA SA.
На основе описания "{description}" придумай цветовую схему для timecyc.
Верни ТОЛЬКО JSON без пояснений:
{{"SkyBottomRGB":[R,G,B],"SkyTopRGB":[R,G,B],"CloudRGB":[R,G,B],"SunCoreRGB":[R,G,B],"AmbientRGB":[R,G,B],"DirectionalRGB":[R,G,B],"FarClip":700.0,"FogStart":100.0}}
Все значения RGB от 0 до 255. FarClip от 300 до 1500. FogStart от 0 до 400."""
    completion = client.chat.completions.create(
        messages=[{"role":"system","content":"Ты генератор JSON для настроек атмосферы игры. Отвечай ТОЛЬКО валидным JSON."},
                  {"role":"user","content":prompt}],
        model="llama-3.1-8b-instant", temperature=0.7)
    raw = completion.choices[0].message.content.strip()
    match = re.search(r'\{[\s\S]*\}', raw)
    if not match: raise ValueError("AI не вернул валидный JSON")
    return json.loads(match.group(0))

def generate_aitimecyc_json(ai_colors: dict) -> str:
    rand_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    output_file_path = f"{rand_string}_aitimecyc.json"
    with open("main.json", "r", encoding='utf-8') as f: timecyc_json_string = f.read()
    replacements = [
        ('"SkyBottomRGB":[SBR016]', f'"SkyBottomRGB":{str(ai_colors["SkyBottomRGB"]).replace(" ","")}'),
        ('"SkyTopRGB":[STR016]', f'"SkyTopRGB":{str(ai_colors["SkyTopRGB"]).replace(" ","")}'),
        ('"CloudRGB":[CLR016]', f'"CloudRGB":{str(ai_colors["CloudRGB"]).replace(" ","")}'),
        ('"SunCoreRGB":[SCR016]', f'"SunCoreRGB":{str(ai_colors["SunCoreRGB"]).replace(" ","")}'),
    ]
    for old_text, new_text in replacements: timecyc_json_string = timecyc_json_string.replace(old_text, new_text)
    with open(output_file_path, "w", encoding='utf-8') as f: f.write(timecyc_json_string)
    return output_file_path

def generate_sky_preview(ai_colors: dict, description: str) -> str:
    width, height = 800, 450
    sky_top = tuple(ai_colors["SkyTopRGB"])
    sky_bottom = tuple(ai_colors["SkyBottomRGB"])
    cloud_color = tuple(ai_colors["CloudRGB"])
    sun_color = tuple(ai_colors["SunCoreRGB"])
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / height
        r = int(sky_top[0] * (1 - t) + sky_bottom[0] * t)
        g = int(sky_top[1] * (1 - t) + sky_bottom[1] * t)
        b = int(sky_top[2] * (1 - t) + sky_bottom[2] * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    sun_x, sun_y = width // 2, height // 5
    sun_radius = 55
    for glow_r in range(sun_radius + 40, sun_radius - 1, -2):
        alpha_ratio = (glow_r - sun_radius) / 40
        glow_color = tuple(int(c + (255 - c) * (1 - alpha_ratio) * 0.3) for c in sun_color[:3])
        draw.ellipse([sun_x - glow_r, sun_y - glow_r, sun_x + glow_r, sun_y + glow_r], fill=glow_color)
    draw.ellipse([sun_x - sun_radius, sun_y - sun_radius, sun_x + sun_radius, sun_y + sun_radius], fill=sun_color[:3])
    for i in range(5):
        cx = random.randint(50, width - 50)
        cy = random.randint(int(height * 0.1), int(height * 0.5))
        for j in range(3):
            cw = random.randint(60, 120); ch = random.randint(20, 40)
            draw.ellipse([cx - cw//2 + j*20, cy - ch//2, cx + cw//2 + j*20, cy + ch//2], fill=cloud_color[:3])
    try: font_small = ImageFont.truetype("arial.ttf", 14)
    except: font_small = ImageFont.load_default()
    colors_info = [("SkyTop", sky_top), ("SkyBot", sky_bottom), ("Cloud", cloud_color), ("Sun", sun_color)]
    sw_x = 10
    for label_text, color in colors_info:
        draw.rectangle([sw_x, height - 55, sw_x + 40, height - 20], fill=color, outline=(255,255,255), width=1)
        draw.text((sw_x, height - 17), label_text, fill=(255, 255, 255), font=font_small)
        sw_x += 95
    rand_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    out_path = f"{rand_str}_sky_preview.png"
    img.save(out_path)
    return out_path

async def kvadratik(hex_color):
    try: FONT = ImageFont.truetype("arial.ttf", 24)
    except: FONT = ImageFont.load_default()
    img_width, img_height = 400, 500
    image = Image.new("RGB", (img_width, img_height), (128, 128, 128))
    draw = ImageDraw.Draw(image)
    rect_width, rect_height = 200, 200
    rect_x = (img_width - rect_width) // 2
    rect_y = 150
    hex_color_val = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color_val[i:i + 2], 16) for i in (0, 2, 4))
    draw.rounded_rectangle([(rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height)], 20, fill=rgb_color, outline=(0, 0, 0), width=2)
    text_color = (0, 0, 0) if sum(rgb_color) > 384 else (255, 255, 255)
    bbox = draw.textbbox((0, 0), hex_color, font=FONT)
    text_x = (img_width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, rect_y + rect_height + 20), hex_color, font=FONT, fill=text_color)
    image_path = f"color_image_{hex_color.replace('#', '')}.png"
    image.save(image_path)
    return image_path

@dp.pre_checkout_query()
async def pre_checkout(query: types.PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def on_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    row = pop_invoice(payload)
    if not row:
        await message.answer(
            "✅ Оплата получена, но возникла ошибка выдачи. Напишите @" + SUPPORT_USERNAME)
        return
    user_id, stars, days = row
    expiry = grant_subscription(user_id, days)

    is_trial = (stars == FREE_TRIAL_STARS and days == FREE_TRIAL_DAYS)
    if is_trial:
        mark_trial_used(user_id)
        plan_label = "3 дня (пробный период)"
    else:
        plan_label = next((p["label"] for p in SUBSCRIPTION_PLANS if p["stars"] == stars), f"{days} дн.")

    # Always log
    log_purchase(user_id, stars, days, plan_label)

    # Referral bonus — only for real paid subs, not trial
    if not is_trial and stars > FREE_TRIAL_STARS:
        ref_result = mark_referral_paid(user_id, stars)
        if ref_result and ref_result[0]:
            referrer_id, reward = ref_result[0], ref_result[1]
            l2_id, l2_reward = ref_result[2], ref_result[3]
            try:
                await bot.send_message(
                    referrer_id,
                    f"🌟 <b>Реферальный бонус!</b>\n"
                    f"Ваш реферал купил Premium — вам начислено <b>{reward}⭐</b>",
                    parse_mode="HTML")
            except Exception:
                pass
            if l2_id and l2_reward:
                try:
                    await bot.send_message(
                        l2_id,
                        f"🌟 <b>Бонус 2-го уровня!</b>\nНачислено <b>{l2_reward}⭐</b>",
                        parse_mode="HTML")
                except Exception:
                    pass
        # Free milestone: 25 total refs → 1 month Pro (for the referrer of this buyer)
        conn_m = sqlite3.connect(DB_PATH)
        cm = conn_m.cursor()
        cm.execute("SELECT referrer_id FROM referrals WHERE referred_id=?", (user_id,))
        ref_row = cm.fetchone(); conn_m.close()
        if ref_row:
            awarded_m, cnt_m = check_free_ref_milestone(ref_row[0])
            if awarded_m:
                try:
                    await bot.send_message(
                        ref_row[0],
                        f"🎁 <b>Поздравляем!</b>\n"
                        f"Вы привели <b>{cnt_m}</b> пользователей — вам выдана Pro-подписка на <b>1 месяц</b>!",
                        parse_mode="HTML")
                except Exception:
                    pass

    until_text = "♾️ бессрочно" if days == -1 else f"до <b>{expiry}</b>"
    await message.answer(
        f"🎉 <b>{'Пробный период' if is_trial else 'Premium'} активирован!</b>\n\n"
        f"💎 Тариф: <b>{plan_label}</b>\n"
        f"📅 Действует: {until_text}\n\n"
        "Все ограничения сняты. Приятного использования!", parse_mode="HTML")

    # Notify all admins
    try:
        conn_adm = sqlite3.connect(DB_PATH)
        cadm = conn_adm.cursor()
        cadm.execute("SELECT chat_id FROM users WHERE admin='True'")
        adm_ids = [r[0] for r in cadm.fetchall()]; conn_adm.close()
        uname_str = message.from_user.username or ""
        name_str = f"@{uname_str}" if uname_str else f"ID:{user_id}"
        trial_tag = " [ПРОБНЫЙ]" if is_trial else ""
        notif = (
            f"💰 <b>Новая покупка!</b>{trial_tag}\n"
            f"👤 {name_str} (<code>{user_id}</code>)\n"
            f"📦 Тариф: <b>{plan_label}</b>\n"
            f"⭐ Звёзд: <b>{stars}</b> | До: <b>{expiry}</b>"
        )
        for adm_id in adm_ids:
            if adm_id != user_id:
                try:
                    await bot.send_message(adm_id, notif, parse_mode="HTML")
                except Exception:
                    pass
    except Exception:
        pass

@dp.callback_query(F.data.startswith("buy_"))
async def cb_buy(callback: types.CallbackQuery, state: FSMContext):
    stars = int(callback.data.split("_")[1])
    plan = next((p for p in SUBSCRIPTION_PLANS if p["stars"] == stars), None)
    if not plan:
        await callback.answer("Тариф не найден", show_alert=True)
        return
    uid = callback.from_user.id
    ref_disc = get_buyer_discount(uid)
    if ref_disc > 0:
        plan = {**plan,
                "stars": max(1, int(plan["stars"] * (1 - ref_disc / 100))),
                "label": plan["label"] + " -" + str(ref_disc) + "% (реферал)",
                "emoji": "👥"}
    await state.set_state(BuyFSM.waiting_promo)
    await state.update_data(pending_plan=plan)
    b = InlineKeyboardBuilder()
    b.button(text="⏭ Пропустить", callback_data="buy_skip_promo")
    await callback.answer()
    await callback.message.answer(
        "🎟 Есть промокод? Введи его или нажми пропустить.\n\n"
        "Цена: <b>" + str(plan["stars"]) + "⭐ — " + plan["label"] + "</b>",
        reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "buy_trial")
async def cb_buy_trial(callback: types.CallbackQuery):
    uid = callback.from_user.id
    if not can_use_trial(uid):
        await callback.answer("❌ Вы уже использовали пробный период", show_alert=True)
        return
    trial_plan = {"stars": FREE_TRIAL_STARS, "days": FREE_TRIAL_DAYS,
                  "label": "3 дня (пробный)", "emoji": "⚡"}
    await callback.answer()
    await send_invoice_for_plan(uid, uid, trial_plan)

@dp.callback_query(F.data == "show_plans")
async def cb_show_plans(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(start_free_text(), reply_markup=kb_subscription_plans(), parse_mode="HTML")

@dp.callback_query(F.data == "buy_skip_promo")
async def cb_buy_skip(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    plan = data.get("pending_plan")
    if not plan:
        await callback.answer("Сессия истекла", show_alert=True)
        return
    await callback.answer()
    await send_invoice_for_plan(callback.from_user.id, callback.from_user.id, plan)

@dp.message(BuyFSM.waiting_promo)
async def fsm_buy_promo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    plan = data.get("pending_plan")
    await state.clear()
    if not plan:
        await message.answer("❌ Сессия истекла, начни заново.")
        return
    code = message.text.strip().upper()
    ok_p, promo, err = use_promo(code, message.from_user.id)
    if not ok_p:
        await message.answer(err + "\n\nОплата без скидки:")
        await send_invoice_for_plan(message.from_user.id, message.from_user.id, plan)
        return
    new_plan = apply_promo_to_plan(plan, promo)
    savings = plan["stars"] - new_plan["stars"]
    await message.answer(
        "✅ <b>Промокод применён!</b>\n"
        "Было: " + str(plan["stars"]) + "⭐ → Стало: <b>" + str(new_plan["stars"]) + "⭐</b>"
        + (" (экономия " + str(savings) + "⭐)" if savings > 0 else ""),
        parse_mode="HTML")
    await send_invoice_for_plan(message.from_user.id, message.from_user.id, new_plan)

@dp.callback_query(F.data == "recheck_channels")
async def cb_recheck(callback: types.CallbackQuery):
    not_sub = await check_required_subs(callback.from_user.id)
    if not_sub:
        await callback.answer("❌ Вы ещё не подписались на все каналы", show_alert=True)
    else:
        await callback.message.edit_text(
            "✅ <b>Подписка подтверждена!</b>\nТеперь вы можете пользоваться ботом. Команды — /help",
            parse_mode="HTML")

@dp.callback_query(F.data == "adm_main")
async def cb_adm_main(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not (row and row[0] == 'True'):
        await callback.answer("❌", show_alert=True); return
    s = get_bot_stats()
    role_label = ROLES.get(get_role(callback.from_user.id), {}).get("label", "👤 Стафф")
    text = (f"🛠 <b>Панель {role_label}</b>\n\n"
            f"👥 Всего: <b>{s['total']}</b> | 💎 Premium: <b>{s['paid']}</b>\n"
            f"🆓 Бесплатных: <b>{s['free']}</b> | 🚫 Банов: <b>{s['banned']}</b>\n"
            f"📅 Активно сегодня: <b>{s['today']}</b>\n"
            f"💾 Work: <b>{get_work_size_gb():.2f} ГБ</b>")
    await callback.message.edit_text(text, reply_markup=kb_admin_main(callback.from_user.id), parse_mode="HTML")

@dp.callback_query(F.data == "adm_stats")
async def cb_adm_stats(callback: types.CallbackQuery):
    s = get_bot_stats()
    top = get_top_users(5)
    c24, s24 = get_purchase_stats(24)
    c7d, s7d = get_purchase_stats(24 * 7)
    c30d, s30d = get_purchase_stats(24 * 30)
    reg24 = get_reg_stats(24)
    reg7d = get_reg_stats(24 * 7)
    t_total, t_open, t_prem_open = get_ticket_stats()
    conn_r = sqlite3.connect(DB_PATH)
    cr = conn_r.cursor()
    cr.execute("SELECT COUNT(*) FROM referrals"); tot_refs = cr.fetchone()[0]
    cr.execute("SELECT COUNT(*) FROM referrals WHERE paid=1"); paid_refs = cr.fetchone()[0]
    cr.execute("SELECT COALESCE(SUM(CAST(ref_balance AS INTEGER)),0) FROM users"); total_bal = cr.fetchone()[0]
    conn_r.close()
    conn_p = sqlite3.connect(DB_PATH)
    cp_cur = conn_p.cursor()
    cp_cur.execute("SELECT COUNT(*) FROM promo_codes WHERE is_active=1"); active_promos = cp_cur.fetchone()[0]
    cp_cur.execute("SELECT COALESCE(SUM(uses),0) FROM promo_codes"); promo_uses = cp_cur.fetchone()[0]
    conn_p.close()
    rev_total, rev_avg = get_review_stats()
    conn_cmd = sqlite3.connect(DB_PATH)
    cc = conn_cmd.cursor()
    today_iso = datetime.datetime.now().strftime("%Y-%m-%d")
    cc.execute("SELECT COUNT(*) FROM command_stats WHERE used_at LIKE ?", (f"{today_iso}%",))
    cmds_today = cc.fetchone()[0]
    cc.execute("SELECT COUNT(*) FROM command_stats"); cmds_total = cc.fetchone()[0]
    conn_cmd.close()
    lines = [
        f"📊 <b>Статистика {BOT_NAME}</b>\n",
        "━━━━ 👥 Пользователи ━━━━",
        f"Всего: <b>{s['total']}</b>  |  Premium: <b>{s['paid']}</b>  |  Free: <b>{s['free']}</b>",
        f"Забанено: <b>{s['banned']}</b>  |  Активны сегодня: <b>{s['today']}</b>",
        f"Новых за 24ч: <b>{reg24}</b>  |  За 7д: <b>{reg7d}</b>",
        "\n━━━━ 💰 Покупки ━━━━",
        f"24ч: <b>{c24}</b> шт / <b>{s24}⭐</b>",
        f"7д: <b>{c7d}</b> / <b>{s7d}⭐</b>  |  30д: <b>{c30d}</b> / <b>{s30d}⭐</b>",
        "\n━━━━ 👥 Рефералы ━━━━",
        f"Всего: <b>{tot_refs}</b>  |  Оплатили: <b>{paid_refs}</b>  |  Баланс: <b>{total_bal}⭐</b>",
        "\n━━━━ 🎟 Промокоды ━━━━",
        f"Активных: <b>{active_promos}</b>  |  Активаций: <b>{promo_uses}</b>",
        "\n━━━━ 🎫 Поддержка ━━━━",
        f"Тикетов: <b>{t_total}</b>  |  Открытых: <b>{t_open}</b>  |  Premium: <b>{t_prem_open}</b>",
        "\n━━━━ 🔢 Команды ━━━━",
        f"Сегодня: <b>{cmds_today}</b>  |  Всего: <b>{cmds_total}</b>",
        "\n━━━━ ⭐ Отзывы ━━━━",
        f"Отзывов: <b>{rev_total}</b>  |  Средняя: <b>{rev_avg}/5</b>",
        f"\n💾 Work: <b>{get_work_size_gb():.2f} ГБ</b>",
        "\n━━━━ 🏆 Топ-5 ━━━━",
    ]
    for i, (uid, uname, cnt) in enumerate(top, 1):
        name = f"@{uname}" if uname else f"ID:{uid}"
        lines.append(f"{i}. {name} — <b>{cnt}</b>")
    b = InlineKeyboardBuilder()
    b.button(text="📈 Графики", callback_data="adm_charts")
    b.button(text="🛒 Покупки", callback_data="adm_purchases")
    b.button(text="🎫 Тикеты", callback_data="adm_tickets")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(2)
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_top")
async def cb_adm_top(callback: types.CallbackQuery):
    rows = get_top_users(15)
    medals = ["🥇","🥈","🥉"]+["🔸"]*12
    lines = ["🏆 <b>Топ-15 активных:</b>\n"]
    for i, (uid, uname, cnt) in enumerate(rows):
        name = f"@{uname}" if uname else f"ID:{uid}"
        lines.append(f"{medals[i]} {i+1}. {name} — <b>{cnt}</b>")
    await callback.message.edit_text("\n".join(lines), reply_markup=kb_back_admin(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_cleanup")
async def cb_adm_cleanup(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not (row and row[0] == 'True'):
        await callback.answer("❌", show_alert=True); return
    before = get_work_size_gb()
    await auto_cleanup()
    after = get_work_size_gb()
    await callback.answer(f"✅ Очищено {before-after:.2f} ГБ, осталось {after:.2f} ГБ", show_alert=True)

@dp.callback_query(F.data == "adm_bans_list")
async def cb_adm_bans(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    adm = c.fetchone()
    if not (adm and adm[0] == 'True'):
        conn.close(); await callback.answer("❌", show_alert=True); return
    c.execute("SELECT chat_id, username, ban_reason FROM users WHERE banned='True' LIMIT 20")
    rows = c.fetchall(); conn.close()
    if not rows:
        await callback.message.edit_text("🚫 <b>Нет заблокированных</b>", reply_markup=kb_back_admin(), parse_mode="HTML"); return
    lines = ["🚫 <b>Заблокированные:</b>\n"]
    for uid, uname, reason in rows:
        name = f"@{uname}" if uname else f"ID:{uid}"
        lines.append(f"• {name} (<code>{uid}</code>) — {reason or '—'}")
    b = InlineKeyboardBuilder()
    b.button(text="🔓 Разбанить по ID", callback_data="adm_do_unban")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(1)
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_do_unban")
async def cb_adm_do_unban(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.unban_id)
    await callback.message.answer("Введите ID пользователя для разбана:")
    await callback.answer()

@dp.message(AdminFSM.unban_id)
async def fsm_unban(message: types.Message, state: FSMContext):
    try:
        uid = int(message.text.strip())
        unban_user(uid)
        await message.answer(f"✅ Пользователь <code>{uid}</code> разбанен.", parse_mode="HTML")
    except ValueError:
        await message.answer("❌ Неверный ID")
    await state.clear()

@dp.callback_query(F.data == "adm_channels")
async def cb_adm_channels(callback: types.CallbackQuery):
    channels = get_required_channels()
    text = ("📣 <b>Обязательные каналы подписки:</b>\n\n" + "\n".join(f"• {ch}" for ch in channels) +
            "\n\n<code>/addchannel @username</code> — добавить\n<code>/delchannel @username</code> — удалить")
    await callback.message.edit_text(text, reply_markup=kb_back_admin(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_broadcast")
async def cb_adm_broadcast(callback: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not (row and row[0] == 'True'):
        await callback.answer("❌", show_alert=True); return
    await state.set_state(AdminFSM.broadcast_text)
    b = InlineKeyboardBuilder()
    b.button(text="❌ Отмена", callback_data="adm_main")
    await callback.message.edit_text(
        "📢 <b>Рассылка</b>\n\nОтправь текст или медиа для рассылки всем пользователям:",
        reply_markup=b.as_markup(), parse_mode="HTML")

@dp.message(AdminFSM.broadcast_text)
async def fsm_broadcast(message: types.Message, state: FSMContext):
    await state.clear()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chat_id FROM users WHERE banned!='True'")
    users = [r[0] for r in c.fetchall()]; conn.close()
    sent = failed = 0
    progress = await message.answer(f"📤 Начинаю рассылку на {len(users)} пользователей...")
    broadcaster_role = get_role(message.from_user.id) or "admin"
    is_anon = broadcaster_role == "developer"
    broadcaster_name = ("@" + message.from_user.username) if message.from_user.username else ("ID:" + str(message.from_user.id))
    sig = "" if is_anon else ("\n\n<i>— " + broadcaster_name + "</i>")
    for uid in users:
        try:
            if message.photo: await message.bot.send_photo(uid, message.photo[-1].file_id, caption=(message.caption or "") + sig)
            elif message.document: await message.bot.send_document(uid, message.document.file_id, caption=(message.caption or "") + sig)
            elif message.text: await message.bot.send_message(uid, message.text + sig, parse_mode="HTML")
            sent += 1
        except: failed += 1
        if (sent + failed) % 50 == 0:
            try: await progress.edit_text(f"📤 Отправлено: {sent} | Ошибок: {failed}")
            except: pass
        await asyncio.sleep(0.05)
    conn2 = sqlite3.connect(DB_PATH)
    c2 = conn2.cursor()
    c2.execute("INSERT INTO broadcasts (text, sent_at, sent_by, total_sent) VALUES (?,?,?,?)",
               (message.text or message.caption or "[медиа]", datetime.datetime.now().isoformat(), message.from_user.id, sent))
    conn2.commit(); conn2.close()
    await progress.edit_text(f"✅ Рассылка завершена!\n📤 Отправлено: {sent}\n❌ Ошибок: {failed}")

@dp.callback_query(F.data == "adm_poll_create")
async def cb_adm_poll(callback: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not (row and row[0] == 'True'):
        await callback.answer("❌", show_alert=True); return
    await state.set_state(AdminFSM.poll_question)
    await callback.message.answer("📋 Введите вопрос для опроса:")
    await callback.answer()

@dp.message(AdminFSM.poll_question)
async def fsm_poll_q(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(AdminFSM.poll_options)
    await message.answer("Введите варианты ответов через запятую (2–10 вариантов):\nПример: Да, Нет, Не знаю")

@dp.message(AdminFSM.poll_options)
async def fsm_poll_opts(message: types.Message, state: FSMContext):
    data = await state.get_data()
    opts = [o.strip() for o in message.text.split(",") if o.strip()]
    if len(opts) < 2 or len(opts) > 10:
        await message.answer("❌ Нужно от 2 до 10 вариантов. Попробуйте ещё раз:"); return
    await state.clear()
    question = data['question']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO polls (question, options, created_at, created_by) VALUES (?,?,?,?)",
              (question, ",".join(opts), datetime.datetime.now().isoformat(), message.from_user.id))
    conn.commit(); conn.close()
    conn2 = sqlite3.connect(DB_PATH)
    c2 = conn2.cursor()
    c2.execute("SELECT chat_id FROM users WHERE banned!='True'")
    users = [r[0] for r in c2.fetchall()]; conn2.close()
    sent = 0
    for uid in users:
        try:
            await message.bot.send_poll(uid, question=question, options=opts, is_anonymous=False)
            sent += 1
        except: pass
        await asyncio.sleep(0.05)
    await message.answer(f"✅ Опрос отправлен {sent} пользователям.")


@dp.callback_query(F.data == "adm_givesub_panel")
async def cb_adm_givesub_panel(callback: types.CallbackQuery, state: FSMContext):
    if not has_perm(callback.from_user.id, "admin"):
        await callback.answer("❌ Нет прав", show_alert=True); return
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="givesub")
    await callback.message.answer(
        "🎁 <b>Выдать подписку</b>\n\nФормат: <code>ID дней</code>\nПример: <code>123456789 30</code>\n-1 = навсегда",
        parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_roles")
async def cb_adm_roles(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "developer"):
        await callback.answer("❌ Только разработчик", show_alert=True); return
    staff = get_all_staff()
    lines = ["👑 <b>Управление ролями</b>\n"]
    if staff:
        for uid, uname, role in staff:
            name = ("@" + uname) if uname else ("ID:" + str(uid))
            lines.append(ROLES.get(role, {}).get("label", role) + " " + name)
    else:
        lines.append("Стаффа пока нет")
    b = InlineKeyboardBuilder()
    b.button(text="➕ Назначить роль", callback_data="adm_role_assign")
    b.button(text="❌ Снять роль", callback_data="adm_role_remove")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(2)
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_role_assign")
async def cb_adm_role_assign(callback: types.CallbackQuery, state: FSMContext):
    if not has_perm(callback.from_user.id, "developer"):
        await callback.answer("❌", show_alert=True); return
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="role_assign")
    await state.update_data(assigner_id=callback.from_user.id)
    await callback.message.answer(
        "Формат: <code>ID роль</code>\nРоли: moderator, admin, developer\nПример: <code>123456 admin</code>",
        parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_role_remove")
async def cb_adm_role_remove(callback: types.CallbackQuery, state: FSMContext):
    if not has_perm(callback.from_user.id, "developer"):
        await callback.answer("❌", show_alert=True); return
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="role_remove")
    await state.update_data(assigner_id=callback.from_user.id)
    await callback.message.answer("Введите ID пользователя для снятия роли:")
    await callback.answer()

@dp.callback_query(F.data == "adm_role_log")
async def cb_adm_role_log(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "developer"):
        await callback.answer("❌", show_alert=True); return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT rl.user_id, u1.username, rl.role, u2.username, rl.assigned_at
                 FROM role_log rl
                 LEFT JOIN users u1 ON rl.user_id=u1.chat_id
                 LEFT JOIN users u2 ON rl.assigned_by=u2.chat_id
                 ORDER BY rl.assigned_at DESC LIMIT 20""")
    rows = c.fetchall(); conn.close()
    lines = ["📋 <b>Лог ролей (последние 20):</b>\n"]
    for uid, uname, role, by_name, at in rows:
        name = ("@" + uname) if uname else ("ID:" + str(uid))
        by = ("@" + by_name) if by_name else "—"
        lines.append("• " + name + " → " + str(role) + " | " + by + " | " + (at[:10] if at else "—"))
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_roles")
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_staff_stats")
async def cb_adm_staff_stats(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "developer"):
        await callback.answer("❌", show_alert=True); return
    staff = get_all_staff()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    lines = ["👮 <b>Активность стаффа</b>\n"]
    for uid, uname, role in staff:
        c.execute("SELECT COUNT(*) FROM support_tickets WHERE closed_by=?", (uid,))
        closed = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM broadcasts WHERE sent_by=?", (uid,))
        broadcasts = c.fetchone()[0]
        name = ("@" + uname) if uname else ("ID:" + str(uid))
        rl = ROLES.get(role, {}).get("label", role)
        lines.append(rl + " " + name + "\n  🎫 закрыто тикетов: " + str(closed) + " | 📢 рассылок: " + str(broadcasts))
    conn.close()
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_main")
    await callback.message.edit_text("\n".join(lines) if len(lines) > 1 else "👮 Нет стаффа",
                                     reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_polls_menu")
async def cb_adm_polls_menu(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "admin"):
        await callback.answer("❌ Нет прав", show_alert=True); return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM polls"); total = c.fetchone()[0]
    conn.close()
    b = InlineKeyboardBuilder()
    b.button(text="📋 Создать опрос", callback_data="adm_poll_create")
    b.button(text="📊 Статистика опросов", callback_data="adm_poll_stats")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(1)
    await callback.message.edit_text(
        "📋 <b>Управление опросами</b>\n\nВсего создано: <b>" + str(total) + "</b>",
        reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_poll_stats")
async def cb_adm_poll_stats(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "admin"):
        await callback.answer("❌", show_alert=True); return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, question, created_at FROM polls ORDER BY created_at DESC LIMIT 10")
    rows = c.fetchall(); conn.close()
    lines = ["📊 <b>Последние опросы:</b>\n"]
    for pid, question, created in rows:
        lines.append("#" + str(pid) + " " + question[:50] + " | " + (created[:10] if created else "—"))
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_polls_menu")
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_prank_menu")
async def cb_adm_prank_menu(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "admin"):
        await callback.answer("❌ Нет прав", show_alert=True); return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM prank_polls"); total = c.fetchone()[0]
    conn.close()
    b = InlineKeyboardBuilder()
    b.button(text="🃏 Создать пранк-опрос", callback_data="adm_prank_create")
    b.button(text="📊 Статистика пранк-опросов", callback_data="adm_prank_stats")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(1)
    await callback.message.edit_text(
        "🃏 <b>Пранк-опросы</b>\n\nВсего создано: <b>" + str(total) + "</b>\n\n"
        "<b>Режимы:</b>\n"
        "• <code>remap</code> — ответ А засчитывается как Б\n"
        "• <code>void</code> — кнопка не работает (ничего не происходит)\n"
        "• <code>reveal</code> — показывает результаты только после ответа",
        reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_prank_create")
async def cb_adm_prank_create(callback: types.CallbackQuery, state: FSMContext):
    if not has_perm(callback.from_user.id, "admin"):
        await callback.answer("❌", show_alert=True); return
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="prank_create")
    await callback.message.answer(
        "🃏 <b>Создание пранк-опроса</b>\n\nФормат (строки):\n"
        "<code>Вопрос\n"
        "Режим: remap / void / reveal\n"
        "Вариант А (что видит),Вариант Б,Вариант В\n"
        "Реальный А (что засчитается),Реальный Б,Реальный В</code>\n\n"
        "Для режима <code>void</code> последняя строка = индексы заблокированных кнопок (напр: 0,2)\n\n"
        "<b>Пример remap:</b>\n"
        "<code>Согласны с условиями?\nremap\nДа,Нет,Воздержусь\nЯ согласен со ВСЕМ,Нет,Воздержусь</code>",
        parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_prank_stats")
async def cb_adm_prank_stats(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "admin"):
        await callback.answer("❌", show_alert=True); return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, question, mode, votes_json, is_active FROM prank_polls ORDER BY created_at DESC LIMIT 10")
    rows = c.fetchall(); conn.close()
    import json as _j
    lines = ["📊 <b>Пранк-опросы:</b>\n"]
    for pid, question, mode, votes_json, active in rows:
        try:
            votes = _j.loads(votes_json or "{}")
            vote_count = len(votes)
        except:
            vote_count = 0
        st = "✅" if active else "❌"
        lines.append(st + " #" + str(pid) + " [" + str(mode) + "] " + question[:40])
        lines.append("   👥 " + str(vote_count) + " голосов")
    b = InlineKeyboardBuilder()
    b.button(text="🔍 Детали опроса", callback_data="adm_prank_detail")
    b.button(text="⬅️ Назад", callback_data="adm_prank_menu")
    b.adjust(1)
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_prank_detail")
async def cb_adm_prank_detail(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="prank_detail")
    await callback.message.answer("Введите ID пранк-опроса:")
    await callback.answer()

@dp.callback_query(F.data == "adm_reviews")
async def cb_adm_reviews(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "admin"):
        await callback.answer("❌", show_alert=True); return
    total_r, avg = get_review_stats()
    reviews = get_reviews(10)
    stars_map = {5: "⭐⭐⭐⭐⭐", 4: "⭐⭐⭐⭐", 3: "⭐⭐⭐", 2: "⭐⭐", 1: "⭐"}
    lines = [
        "⭐ <b>Отзывы</b>\n",
        "Всего: <b>" + str(total_r) + "</b> | Средняя оценка: <b>" + str(avg) + "</b>\n",
        "─────────────────"
    ]
    for uid, uname, rating, text, created in reviews:
        name = ("@" + uname) if uname else ("ID:" + str(uid))
        lines.append(stars_map.get(rating, str(rating) + "⭐") + " " + name)
        if text:
            lines.append("  " + text[:100])
        lines.append("  " + (created[:10] if created else ""))
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_main")
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data.startswith("prank_vote_"))
async def cb_prank_vote(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    poll_id = int(parts[2])
    chosen_idx = int(parts[3])
    poll = get_prank_poll(poll_id)
    if not poll or not poll["is_active"]:
        await callback.answer("❌ Опрос закрыт", show_alert=True); return
    mode = poll["mode"]
    if mode == "void":
        blocked = poll.get("mapped_options", [])
        try:
            void_indices = [int(x) for x in blocked if str(x).isdigit()]
        except:
            void_indices = []
        if chosen_idx in void_indices:
            await callback.answer("", show_alert=False); return
        await callback.answer("✅ Голос засчитан!", show_alert=False)
        return
    real_idx = record_prank_vote(poll_id, callback.from_user.id, chosen_idx)
    if mode == "remap":
        real_opt = poll["mapped_options"][real_idx] if real_idx < len(poll["mapped_options"]) else "?"
        await callback.answer("✅ Ваш ответ: " + real_opt, show_alert=True)
    elif mode == "reveal":
        stats = get_prank_poll_stats(poll_id)
        lines = ["📊 Результаты:\n"]
        total_v = sum(stats.values()) or 1
        for opt, cnt in stats.items():
            pct = round(cnt / total_v * 100)
            bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
            lines.append(opt[:20] + ": " + bar + " " + str(pct) + "%")
        await callback.answer("\n".join(lines), show_alert=True)


@dp.callback_query(F.data.startswith("promo_apply_"))
async def cb_promo_apply(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    stars = int(parts[2])
    code = "_".join(parts[3:])
    uid = callback.from_user.id
    p = get_promo(code)
    if not p:
        await callback.answer("❌ Промокод недействителен", show_alert=True)
        return
    plan = next((pl for pl in SUBSCRIPTION_PLANS if pl["stars"] == stars), None)
    if not plan:
        await callback.answer("Тариф не найден", show_alert=True)
        return
    new_plan = apply_promo_to_plan(plan, p)
    await callback.answer()
    await send_invoice_for_plan(uid, uid, new_plan)


# ─── Тех. поддержка: пользователь ────────────────────────────────────
@dp.callback_query(F.data == "support_new")
async def cb_support_new(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SupportFSM.subject)
    await callback.message.answer("📝 Введите тему обращения (коротко, 1 строка):")
    await callback.answer()

@dp.message(SupportFSM.subject)
async def fsm_support_subject(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text.strip())
    await state.set_state(SupportFSM.message)
    await message.answer("✉️ Опишите проблему подробнее:")

@dp.message(SupportFSM.message)
async def fsm_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    uid = message.from_user.id
    uname = message.from_user.username or ""
    is_sub, _ = find_user_data_in_sql(uid)
    tid = create_ticket(uid, uname, is_sub, data["subject"], message.text.strip())
    prio = "💎 PREMIUM" if is_sub else "🆓 FREE"
    await message.answer(
        "✅ <b>Обращение #" + str(tid) + " отправлено!</b>\\n\\n"
        "Мы ответим в ближайшее время. Приоритет: " + prio,
        parse_mode="HTML")
    for adm_id in loging_id:
        try:
            await bot.send_message(adm_id,
                "🎫 <b>Новый тикет #" + str(tid) + "</b>  " + prio + "\\n"
                "👤 @" + uname + " (<code>" + str(uid) + "</code>)\\n"
                "📌 " + data["subject"] + "\\n"
                "💬 " + message.text.strip()[:200],
                parse_mode="HTML")
        except: pass

# ─── Тех. поддержка: admin ───────────────────────────────────────────
@dp.callback_query(F.data == "adm_tickets")
async def cb_adm_tickets(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not (row and row[0] == "True"):
        await callback.answer("❌", show_alert=True); return
    total_t, open_t, prem_open = get_ticket_stats()
    tickets = get_open_tickets()
    lines = [
        "🎫 <b>Тех. поддержка</b>\\n",
        "Всего: <b>" + str(total_t) + "</b> | Открытых: <b>" + str(open_t) + "</b> | Premium открытых: <b>" + str(prem_open) + "</b>\\n",
    ]
    if not tickets:
        lines.append("✅ Нет открытых тикетов")
    else:
        lines.append("─────────────────")
        for tid, uid, uname, is_prem, subj, status, created in tickets[:15]:
            prio = "💎" if is_prem else "🆓"
            name = ("@" + uname) if uname else ("ID:" + str(uid))
            lines.append(prio + " #" + str(tid) + " " + name + "\\n   " + subj[:50])
    b = InlineKeyboardBuilder()
    b.button(text="↩️ Ответить/закрыть тикет", callback_data="adm_ticket_reply")
    b.button(text="📋 Все тикеты", callback_data="adm_tickets_all")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(1)
    await callback.message.edit_text("\\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_ticket_reply")
async def cb_adm_ticket_reply(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.ticket_reply)
    await callback.message.answer("Введите: <номер_тикета> <ответ>\\nПример: 5 Проблема решена, попробуйте снова")
    await callback.answer()

@dp.message(AdminFSM.ticket_reply)
async def fsm_ticket_reply(message: types.Message, state: FSMContext):
    await state.clear()
    parts = message.text.strip().split(" ", 1)
    if len(parts) < 2:
        await message.answer("❌ Формат: <id> <ответ>"); return
    try:
        tid = int(parts[0])
    except:
        await message.answer("❌ ID должен быть числом"); return
    reply_text = parts[1]
    ticket = get_ticket(tid)
    if not ticket:
        await message.answer("❌ Тикет #" + str(tid) + " не найден"); return
    close_ticket(tid, message.from_user.id, reply_text)
    uid = ticket[1]
    try:
        await bot.send_message(uid,
            "📬 <b>Ответ на ваше обращение #" + str(tid) + "</b>\\n\\n" + reply_text + "\\n\\n"
            "<i>Служба поддержки " + BOT_NAME + "</i>",
            parse_mode="HTML")
    except: pass
    await message.answer("✅ Тикет #" + str(tid) + " закрыт, ответ отправлен.")

@dp.callback_query(F.data == "adm_tickets_all")
async def cb_adm_tickets_all(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id,user_id,username,is_premium,subject,status,created_at FROM support_tickets ORDER BY created_at DESC LIMIT 20")
    rows = c.fetchall(); conn.close()
    lines = ["📋 <b>Все тикеты (последние 20):</b>\\n"]
    for tid, uid, uname, is_p, subj, status, created in rows:
        prio = "💎" if is_p else "🆓"
        st = "✅" if status == "closed" else "🔓"
        name = ("@" + uname) if uname else ("ID:" + str(uid))
        lines.append(st + prio + " #" + str(tid) + " " + name + " — " + subj[:40] + "  " + (created[:10] if created else ""))
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_tickets")
    await callback.message.edit_text("\\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

# ─── История покупок: admin ───────────────────────────────────────────
@dp.callback_query(F.data == "adm_purchases")
async def cb_adm_purchases(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not (row and row[0] == "True"):
        await callback.answer("❌", show_alert=True); return
    count_24, sum_24 = get_purchase_stats(24)
    count_7d, sum_7d = get_purchase_stats(24*7)
    count_30d, sum_30d = get_purchase_stats(24*30)
    history = get_purchase_history(limit=15)
    lines = [
        "🛒 <b>История покупок</b>\\n",
        "За 24ч: <b>" + str(count_24) + "</b> покупок / <b>" + str(sum_24) + "⭐</b>",
        "За 7 дней: <b>" + str(count_7d) + "</b> / <b>" + str(sum_7d) + "⭐</b>",
        "За 30 дней: <b>" + str(count_30d) + "</b> / <b>" + str(sum_30d) + "⭐</b>\\n",
        "─────────────────",
    ]
    for row2 in history:
        pid, uid, st, days, label, promo, disc, created, uname = row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6], row2[7], row2[9] if len(row2) > 9 else ""
        name = ("@" + uname) if uname else ("ID:" + str(uid))
        promo_str = " 🎟" + str(promo) if promo else ""
        lines.append("• " + name + " — " + str(st) + "⭐ " + (label or "") + promo_str + " | " + (created[:10] if created else ""))
    b = InlineKeyboardBuilder()
    b.button(text="👤 Покупки пользователя", callback_data="adm_user_purchases")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(1)
    await callback.message.edit_text("\\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_user_purchases")
async def cb_adm_user_purchases(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="user_purchases")
    await callback.message.answer("Введите ID пользователя:")
    await callback.answer()

# ─── Графики: admin ───────────────────────────────────────────────────
# ── Chart helpers ─────────────────────────────────────────────────────────────

def _period_kb(type_key: str):
    """Keyboard with period options for a given chart type."""
    b = InlineKeyboardBuilder()
    for lbl, p in [("1ч","hour"),("24ч","day"),("7д","week"),
                   ("1м","month"),("3м","quarter"),("1г","year")]:
        b.button(text=lbl, callback_data=f"adm_chart_{type_key}_{p}")
    b.button(text="⬅️ Назад", callback_data="adm_charts")
    b.adjust(3)
    return b.as_markup()

def _get_buckets(table: str, ts_col: str, period: str,
                 extra_where: str = "", val_col: str = None) -> dict:
    """Generic time-bucketed counter from any table."""
    ph = {"hour":(1,"%H:%M"),"day":(24,"%H:00"),"week":(168,"%d.%m"),
          "month":(720,"%d.%m"),"quarter":(2160,"%m.%Y"),"year":(8760,"%m.%Y")}
    hours, fmt = ph.get(period, (168, "%d.%m"))
    since = (datetime.datetime.now() - datetime.timedelta(hours=hours)).isoformat()
    where = f"WHERE {ts_col} >= '{since}'"
    if extra_where:
        where += f" AND {extra_where}"
    sel = f"{ts_col},{val_col}" if val_col else ts_col
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"SELECT {sel} FROM {table} {where} ORDER BY {ts_col}")
    rows = c.fetchall(); conn.close()
    buckets: dict = {}
    for row in rows:
        try:
            dt = datetime.datetime.fromisoformat(row[0])
            key = dt.strftime(fmt)
            val = (row[1] or 0) if val_col else 1
            buckets[key] = buckets.get(key, 0) + val
        except Exception:
            pass
    return buckets

def _bar_chart(title: str, buckets: dict, suffix: str = "", width: int = 10) -> str:
    if not buckets:
        return title + "\n\n<i>Нет данных за этот период</i>"
    items = list(buckets.items())[-20:]
    mx = max(v for _, v in items) or 1
    lines = [title + "\n"]
    for lbl, val in items:
        filled = round(val / mx * width)
        bar = "█" * filled + "░" * (width - filled)
        lines.append(f"<code>{lbl[:7].ljust(7)} |{bar}| {val}{suffix}</code>")
    return "\n".join(lines)

# ── Chart callbacks ────────────────────────────────────────────────────────────

@dp.callback_query(F.data == "adm_charts")
async def cb_adm_charts(callback: types.CallbackQuery):
    if not has_perm(callback.from_user.id, "moderator"):
        await callback.answer("❌ Нет прав", show_alert=True); return
    b = InlineKeyboardBuilder()
    b.button(text="👥 Регистрации",  callback_data="adm_chart_type_reg")
    b.button(text="💰 Покупки",      callback_data="adm_chart_type_purchases")
    b.button(text="👥 Рефералы",     callback_data="adm_chart_type_refs")
    b.button(text="🎟 Промокоды",    callback_data="adm_chart_type_promos")
    b.button(text="🎫 Тикеты",       callback_data="adm_chart_type_tickets")
    b.button(text="🔢 Команды",      callback_data="adm_chart_cmds")
    b.button(text="⬅️ Назад",        callback_data="adm_main")
    b.adjust(2)
    await callback.message.edit_text(
        "📈 <b>Графики</b>\n\nВыберите тип статистики:",
        reply_markup=b.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("adm_chart_type_"))
async def cb_adm_chart_type(callback: types.CallbackQuery):
    type_key = callback.data.replace("adm_chart_type_", "")
    names = {"reg": "👥 Регистрации", "purchases": "💰 Покупки",
             "refs": "👥 Рефералы", "promos": "🎟 Промокоды", "tickets": "🎫 Тикеты"}
    await callback.message.edit_text(
        f"📈 <b>{names.get(type_key, type_key)}</b>\n\nВыберите период:",
        reply_markup=_period_kb(type_key), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("adm_chart_reg_"))
async def cb_adm_chart_reg(callback: types.CallbackQuery):
    period = callback.data.replace("adm_chart_reg_", "")
    buckets = _get_buckets("registrations", "registered_at", period)
    text = _bar_chart("📊 <b>Регистрации</b>", buckets)
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_chart_type_reg")
    await callback.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("adm_chart_purchases_"))
async def cb_adm_chart_purchases_period(callback: types.CallbackQuery):
    period = callback.data.replace("adm_chart_purchases_", "")
    cnt_b = _get_buckets("purchases", "created_at", period)
    star_b = _get_buckets("purchases", "created_at", period, val_col="stars")
    if not cnt_b:
        await callback.answer("Нет данных за этот период", show_alert=True); return
    items = list(cnt_b.items())[-14:]
    mx = max(v for _, v in items) or 1
    lines = ["💰 <b>Покупки</b>\n"]
    for key, cnt in items:
        filled = round(cnt / mx * 10)
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(f"<code>{key.ljust(6)} |{bar}| {cnt}шт {star_b.get(key,0)}⭐</code>")
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_chart_type_purchases")
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("adm_chart_refs_"))
async def cb_adm_chart_refs(callback: types.CallbackQuery):
    period = callback.data.replace("adm_chart_refs_", "")
    all_b  = _get_buckets("referrals", "created_at", period)
    paid_b = _get_buckets("referrals", "created_at", period, extra_where="paid=1")
    if not all_b:
        await callback.answer("Нет данных за этот период", show_alert=True); return
    items = list(all_b.items())[-20:]
    mx = max(v for _, v in items) or 1
    lines = ["👥 <b>Рефералы</b>\n"]
    for key, cnt in items:
        filled = round(cnt / mx * 10)
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(f"<code>{key.ljust(6)} |{bar}| {cnt} ({paid_b.get(key,0)}💰)</code>")
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_chart_type_refs")
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("adm_chart_promos_"))
async def cb_adm_chart_promos(callback: types.CallbackQuery):
    period = callback.data.replace("adm_chart_promos_", "")
    buckets = _get_buckets("promo_uses", "used_at", period)
    text = _bar_chart("🎟 <b>Активации промокодов</b>", buckets)
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_chart_type_promos")
    await callback.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("adm_chart_tickets_"))
async def cb_adm_chart_tickets(callback: types.CallbackQuery):
    period = callback.data.replace("adm_chart_tickets_", "")
    all_b    = _get_buckets("support_tickets", "created_at", period)
    closed_b = _get_buckets("support_tickets", "created_at", period, extra_where="status='closed'")
    if not all_b:
        await callback.answer("Нет данных за этот период", show_alert=True); return
    items = list(all_b.items())[-20:]
    mx = max(v for _, v in items) or 1
    lines = ["🎫 <b>Тикеты</b>\n"]
    for key, cnt in items:
        filled = round(cnt / mx * 10)
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(f"<code>{key.ljust(6)} |{bar}| {cnt} ({closed_b.get(key,0)}✅)</code>")
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_chart_type_tickets")
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_chart_cmds")
async def cb_adm_chart_cmds(callback: types.CallbackQuery):
    stats = get_command_stats(20)
    if not stats:
        await callback.answer("Нет данных", show_alert=True); return
    max_v = stats[0][1] if stats else 1
    lines = ["🔢 <b>Топ команд за всё время:</b>\n"]
    for cmd, cnt in stats:
        filled = round(cnt / max_v * 10)
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(f"<code>{cmd[:12].ljust(12)} |{bar}| {cnt}</code>")
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад", callback_data="adm_charts")
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "adm_promos")
async def cb_adm_promos(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not has_perm(callback.from_user.id, "moderator"):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    conn2 = sqlite3.connect(DB_PATH)
    c2 = conn2.cursor()
    c2.execute("SELECT COUNT(*) FROM promo_codes")
    total_promos = c2.fetchone()[0]
    c2.execute("SELECT COUNT(*) FROM promo_codes WHERE is_active=1")
    active_promos = c2.fetchone()[0]
    c2.execute("SELECT SUM(uses) FROM promo_codes")
    total_uses = c2.fetchone()[0] or 0
    c2.execute("SELECT code, name, discount_pct, custom_stars, custom_days, uses, max_uses, expires_at, is_active FROM promo_codes ORDER BY uses DESC")
    promos = c2.fetchall()
    conn2.close()
    lines = [
        "🎟 <b>Управление промокодами</b>\n",
        "Всего: <b>" + str(total_promos) + "</b> | Активных: <b>" + str(active_promos) + "</b> | Всего активаций: <b>" + str(total_uses) + "</b>\n",
    ]
    if promos:
        lines.append("─────────────────────")
        for code, name, disc, cstars, cdays, uses, max_uses, exp, active in promos:
            status = "✅" if active else "❌"
            limit = str(uses) + "/" + (str(max_uses) if max_uses else "∞")
            if cstars:
                price_info = str(cstars) + "⭐/" + str(cdays) + "д"
            elif disc:
                price_info = "-" + str(disc) + "%"
            else:
                price_info = "—"
            exp_str = exp[:10] if exp else "∞"
            lines.append(status + " <code>" + code + "</code> <i>" + (name or "") + "</i>")
            lines.append("   " + price_info + " | использ: " + limit + " | до " + exp_str)
    b = InlineKeyboardBuilder()
    b.button(text="➕ Создать", callback_data="adm_promo_create")
    b.button(text="❌ Деактивировать", callback_data="adm_promo_deact")
    b.button(text="🔄 Заменить промокод", callback_data="adm_promo_replace")
    b.button(text="🔍 Детали кода", callback_data="adm_promo_detail")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(2)
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "adm_promo_detail")
async def cb_adm_promo_detail(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="detail")
    await callback.message.answer("Введите код промокода для просмотра деталей:")
    await callback.answer()

@dp.callback_query(F.data == "adm_promo_create")
async def cb_adm_promo_create(callback: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not has_perm(callback.from_user.id, "moderator"):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    await state.set_state(AdminFSM.promo_create)
    lines_ex = [
        "КОД",
        "Название",
        "Комментарий (или -)",
        "Ссылка (или -)",
        "Скидка % (0 = нет)",
        "Кастом цена Stars (0 = нет)",
        "Кастом дней (0 = стандарт)",
        "Макс. использований (0 = ∞)",
        "Дата истечения ДД.ММ.ГГГГ (или -)",
    ]
    example_lines = [
        "SUMMER25",
        "Летняя акция",
        "Скидка для новых",
        "https://t.me/pweper",
        "25",
        "0",
        "0",
        "100",
        "31.08.2025",
    ]
    instr = ("🎟 <b>Создание промокода</b>\n\n"
             "Отправь 9 строк:\n<code>" +
             "\n".join(lines_ex) + "</code>\n\n"
             "<b>Пример:</b>\n<code>" +
             "\n".join(example_lines) + "</code>")
    await callback.message.answer(instr, parse_mode="HTML")
    await callback.answer()

@dp.message(AdminFSM.promo_create)
async def fsm_promo_create(message: types.Message, state: FSMContext):
    await state.clear()
    lines = [l.strip() for l in message.text.strip().split("\n")]
    if len(lines) < 9:
        await message.answer("❌ Нужно 9 строк. Отмена.")
        return
    code = lines[0]
    name = lines[1]
    comment = None if lines[2] == "-" else lines[2]
    link    = None if lines[3] == "-" else lines[3]
    try:
        disc   = int(lines[4])
        cstars = int(lines[5])
        cdays  = int(lines[6])
        max_u  = int(lines[7])
    except ValueError:
        await message.answer("❌ Строки 5–8 должны быть числами.")
        return
    exp = None
    if lines[8] != "-":
        try:
            exp = datetime.datetime.strptime(lines[8], "%d.%m.%Y").isoformat()
        except:
            await message.answer("❌ Дата: ДД.ММ.ГГГГ")
            return
    ok_c, err = create_promo(code, name, comment, link, disc, cstars, cdays,
                             max_u, exp, message.from_user.id)
    if ok_c:
        info = []
        if cstars:
            info.append("💰 Цена: " + str(cstars) + "⭐ / " +
                        (str(cdays) if cdays else "стандарт") + " дн.")
        elif disc:
            info.append("💸 Скидка: -" + str(disc) + "%")
        if max_u:
            info.append("🔢 Лимит: " + str(max_u))
        if exp:
            info.append("📅 До: " + lines[8])
        await message.answer(
            "✅ <b>Промокод создан!</b>\n🎟 <code>" + code.upper() + "</code> — " + name +
            ("\n" + "\n".join(info) if info else ""),
            parse_mode="HTML")
    else:
        await message.answer("❌ " + str(err))

@dp.callback_query(F.data == "adm_promo_deact")
async def cb_adm_promo_deact(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="deact")
    await callback.message.answer("Введите код промокода для деактивации:")
    await callback.answer()

@dp.callback_query(F.data == "adm_promo_replace")
async def cb_adm_promo_replace(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="replace_promo")
    await callback.message.answer(
        "🔄 <b>Замена промокода</b>\n\n"
        "Введите две строки:\n"
        "<code>СТАРЫЙ_КОД</code>\n"
        "<code>НОВЫЙ_КОД</code>\n\n"
        "Старый будет деактивирован, у всех пользователей "
        "активируется новый.",
        parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_ref_user")
async def cb_adm_ref_user(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminFSM.promo_code_input)
    await state.update_data(promo_action="ref_user")
    await callback.message.answer("Введите ID или @username пользователя:")
    await callback.answer()


@dp.message(AdminFSM.promo_code_input)
async def fsm_promo_code_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    code = message.text.strip().upper()
    action = data.get("promo_action", "")
    if action == "deact":
        if deactivate_promo(code):
            await message.answer("✅ Промокод <code>" + code + "</code> деактивирован.", parse_mode="HTML")
        else:
            await message.answer("❌ Промокод <code>" + code + "</code> не найден.", parse_mode="HTML")
    elif action == "replace_promo":
        lines_rp = [l.strip() for l in message.text.strip().splitlines() if l.strip()]
        if len(lines_rp) < 2:
            await message.answer("❌ Нужно две строки: старый код и новый код"); return
        old_code, new_code = lines_rp[0].upper(), lines_rp[1].upper()
        old_p = get_promo(old_code)
        new_p = get_promo(new_code)
        if not old_p:
            await message.answer(f"❌ Промокод <code>{old_code}</code> не найден или неактивен.", parse_mode="HTML"); return
        if not new_p:
            await message.answer(f"❌ Промокод <code>{new_code}</code> не найден или неактивен.", parse_mode="HTML"); return
        deactivate_promo(old_code)
        conn_rp = sqlite3.connect(DB_PATH)
        c_rp = conn_rp.cursor()
        c_rp.execute("UPDATE users SET active_promo=?, promo_expires=? WHERE active_promo=?",
                     (new_code, new_p["expires_at"], old_code))
        affected = c_rp.rowcount
        conn_rp.commit(); conn_rp.close()
        await message.answer(
            f"✅ <b>Промокод заменён!</b>\n"
            f"<code>{old_code}</code> → <code>{new_code}</code>\n"
            f"Обновлено пользователей: <b>{affected}</b>",
            parse_mode="HTML")
    elif action == "detail":
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM promo_codes WHERE code=?", (code,))
        row = c.fetchone()
        c.execute("SELECT u.username, u.chat_id, pu.used_at FROM promo_uses pu LEFT JOIN users u ON pu.user_id=u.chat_id WHERE pu.code=? ORDER BY pu.used_at DESC LIMIT 15", (code,))
        uses_list = c.fetchall()
        conn.close()
        if not row:
            await message.answer("❌ Промокод не найден.")
            return
        keys = ["id","code","name","comment","link","discount_pct","custom_stars","custom_days","max_uses","uses","expires_at","is_active","created_by","created_at"]
        p = dict(zip(keys, row))
        lines = [
            "🎟 <b>Промокод: <code>" + p["code"] + "</code></b>",
            "Статус: " + ("✅ Активен" if p["is_active"] else "❌ Деактивирован"),
            "Название: " + (p["name"] or "—"),
            "Комментарий: " + (p["comment"] or "—"),
            "Ссылка: " + (p["link"] or "—"),
        ]
        if p["custom_stars"]:
            lines.append("Цена: " + str(p["custom_stars"]) + "⭐ / " + str(p["custom_days"]) + " дн.")
        elif p["discount_pct"]:
            lines.append("Скидка: -" + str(p["discount_pct"]) + "%")
        lines.append("Использований: <b>" + str(p["uses"]) + "</b>" + ("/" + str(p["max_uses"]) if p["max_uses"] else "/∞"))
        lines.append("Истекает: " + (p["expires_at"][:10] if p["expires_at"] else "∞"))
        lines.append("Создан: " + (p["created_at"][:10] if p["created_at"] else "—"))
        if uses_list:
            lines.append("\n👤 <b>Последние активации:</b>")
            for uname, uid, used_at in uses_list:
                name = ("@" + uname) if uname else ("ID:" + str(uid))
                lines.append("• " + name + " — " + (used_at[:16] if used_at else "—"))
        await message.answer("\n".join(lines), parse_mode="HTML")
    elif action == "ref_user":
        query = code
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if query.startswith("@"):
            c.execute("SELECT chat_id FROM users WHERE username=?", (query[1:],))
        else:
            try:
                c.execute("SELECT chat_id FROM users WHERE chat_id=?", (int(query),))
            except:
                conn.close()
                await message.answer("❌ Неверный ID")
                return
        uid_row = c.fetchone()
        if not uid_row:
            conn.close()
            await message.answer("❌ Пользователь не найден")
            return
        uid = uid_row[0]
        c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (uid,))
        tot = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=? AND paid=1", (uid,))
        paid_r = c.fetchone()[0]
        c.execute("SELECT COALESCE(CAST(ref_balance AS INTEGER),0) FROM users WHERE chat_id=?", (uid,))
        bal = c.fetchone()[0]
        c.execute("SELECT referred_by FROM users WHERE chat_id=?", (uid,))
        ref_by = c.fetchone()
        c.execute("""SELECT u2.username, u2.chat_id, r.paid, r.reward_given, r.created_at
                     FROM referrals r LEFT JOIN users u2 ON r.referred_id=u2.chat_id
                     WHERE r.referrer_id=? ORDER BY r.created_at DESC LIMIT 20""", (uid,))
        refs = c.fetchall()
        conn.close()
        lines_u = [
            "👤 <b>Рефералы пользователя ID:" + str(uid) + "</b>\n",
            "Приглашено: <b>" + str(tot) + "</b> | Оплатили: <b>" + str(paid_r) + "</b>",
            "Баланс: <b>" + str(bal) + "⭐</b>",
            "Сам приглашён: " + (("ID:" + str(ref_by[0])) if ref_by and ref_by[0] else "нет") + "\n",
            "📋 <b>Список рефералов:</b>"
        ]
        for uname2, uid2, is_paid, rew, created in refs:
            nm = ("@" + uname2) if uname2 else ("ID:" + str(uid2))
            status2 = "✅" if is_paid else "⏳"
            lines_u.append(status2 + " " + nm + " +" + str(rew or 0) + "⭐ | " + (created[:10] if created else "—"))
        await message.answer("\n".join(lines_u), parse_mode="HTML")
    elif action == "user_purchases":
        try:
            uid_p = int(code)
        except:
            await message.answer("❌ ID должен быть числом"); return
        rows_p = get_purchase_history(user_id=uid_p, limit=20)
        if not rows_p:
            await message.answer("Покупок не найдено."); return
        lines_p = ["🛒 <b>Покупки ID:" + str(uid_p) + "</b>\n"]
        for row_p in rows_p:
            pid, uid2, st, days2, label, promo2, disc2, created2 = row_p[:8]
            promo_s = " 🎟" + str(promo2) if promo2 else ""
            lines_p.append("• " + str(st) + "⭐ " + (label or "") + promo_s + " | " + (created2[:10] if created2 else ""))
        await message.answer("\n".join(lines_p), parse_mode="HTML")
    elif action == "givesub":
        parts = code.split()
        if len(parts) < 2:
            await message.answer("❌ Формат: ID дней"); return
        try:
            uid_g = int(parts[0]); days_g = int(parts[1])
        except:
            await message.answer("❌ ID и дни должны быть числами"); return
        expiry_g = grant_subscription(uid_g, days_g)
        log_purchase(uid_g, 0, days_g, "Admin gift", None, 0)
        await message.answer("✅ Подписка выдана <code>" + str(uid_g) + "</code> до <b>" + expiry_g + "</b>", parse_mode="HTML")
        try:
            await bot.send_message(uid_g,
                "🎁 <b>Вам выдана подписка!</b>\n📅 Действует до: <b>" + expiry_g + "</b>",
                parse_mode="HTML")
        except: pass
    elif action == "role_assign":
        data2 = await state.get_data() if False else {}
        parts_r = code.split()
        if len(parts_r) < 2:
            await message.answer("❌ Формат: ID роль"); return
        try:
            uid_r = int(parts_r[0])
        except:
            await message.answer("❌ ID должен быть числом"); return
        role_r = parts_r[1].lower()
        if role_r not in ROLES:
            await message.answer("❌ Роли: moderator, admin, developer"); return
        assigner_lvl = get_role_level(message.from_user.id)
        target_lvl = ROLES.get(role_r, {}).get("level", 0)
        if target_lvl >= assigner_lvl:
            await message.answer("❌ Нельзя назначить роль равную или выше вашей"); return
        if set_role(uid_r, role_r, message.from_user.id):
            rl = ROLES[role_r]["label"]
            await message.answer("✅ Пользователю <code>" + str(uid_r) + "</code> назначена роль " + rl, parse_mode="HTML")
            try:
                await bot.send_message(uid_r, "👑 Вам назначена роль <b>" + rl + "</b> в " + BOT_NAME, parse_mode="HTML")
            except: pass
        else:
            await message.answer("❌ Пользователь не найден в БД")
    elif action == "role_remove":
        try:
            uid_rm = int(code)
        except:
            await message.answer("❌ ID должен быть числом"); return
        assigner_lvl = get_role_level(message.from_user.id)
        cur_role = get_role(uid_rm)
        cur_lvl = ROLES.get(cur_role, {}).get("level", 0)
        if cur_lvl >= assigner_lvl:
            await message.answer("❌ Нельзя снять роль равную или выше вашей"); return
        set_role(uid_rm, "none", message.from_user.id)
        await message.answer("✅ Роль снята с пользователя <code>" + str(uid_rm) + "</code>", parse_mode="HTML")
    elif action == "prank_create":
        lines_pc = [l.strip() for l in code.split("\n")]
        if len(lines_pc) < 4:
            await message.answer("❌ Нужно 4 строки: вопрос, режим, варианты, реальные варианты"); return
        q_pc = lines_pc[0]
        mode_pc = lines_pc[1].lower()
        if mode_pc not in ("remap", "void", "reveal"):
            await message.answer("❌ Режим: remap / void / reveal"); return
        real_opts = [o.strip() for o in lines_pc[2].split(",") if o.strip()]
        mapped_opts = [o.strip() for o in lines_pc[3].split(",") if o.strip()]
        if len(real_opts) < 2:
            await message.answer("❌ Минимум 2 варианта"); return
        pid_pc = create_prank_poll(q_pc, real_opts, mapped_opts, mode_pc, message.from_user.id)
        b_pc = InlineKeyboardBuilder()
        for i, opt in enumerate(real_opts):
            b_pc.button(text=opt, callback_data="prank_vote_" + str(pid_pc) + "_" + str(i))
        b_pc.adjust(1)
        conn_pc = sqlite3.connect(DB_PATH)
        cur_pc = conn_pc.cursor()
        cur_pc.execute("SELECT chat_id FROM users WHERE banned!='True'")
        users_pc = [r[0] for r in cur_pc.fetchall()]; conn_pc.close()
        sent_pc = 0
        for uid_pc in users_pc:
            try:
                await bot.send_message(uid_pc, "🃏 <b>" + q_pc + "</b>", reply_markup=b_pc.as_markup(), parse_mode="HTML")
                sent_pc += 1
            except: pass
            await asyncio.sleep(0.05)
        await message.answer("✅ Пранк-опрос #" + str(pid_pc) + " разослан " + str(sent_pc) + " пользователям.")
    elif action == "prank_detail":
        try:
            pid_d = int(code)
        except:
            await message.answer("❌ ID опроса"); return
        poll_d = get_prank_poll(pid_d)
        if not poll_d:
            await message.answer("❌ Опрос не найден"); return
        stats_d = get_prank_poll_stats(pid_d)
        total_v = sum(stats_d.values()) or 1
        lines_d = [
            "🃏 <b>Пранк-опрос #" + str(pid_d) + "</b>",
            "Вопрос: " + poll_d["question"],
            "Режим: " + poll_d["mode"],
            "Голосов: " + str(len(poll_d["votes_json"])) + "\n",
            "📊 <b>Реальные результаты:</b>"
        ]
        for opt, cnt in stats_d.items():
            pct = round(cnt / total_v * 100)
            bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
            lines_d.append(opt[:25] + ": " + bar + " " + str(pct) + "% (" + str(cnt) + ")")
        await message.answer("\n".join(lines_d), parse_mode="HTML")

@dp.callback_query(F.data == "adm_ref_stats")
async def cb_adm_ref_stats(callback: types.CallbackQuery):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT admin FROM users WHERE chat_id=?", (callback.from_user.id,))
    row = c.fetchone(); conn.close()
    if not has_perm(callback.from_user.id, "moderator"):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    conn2 = sqlite3.connect(DB_PATH)
    c2 = conn2.cursor()
    c2.execute("SELECT COUNT(*) FROM referrals")
    total = c2.fetchone()[0]
    c2.execute("SELECT COUNT(*) FROM referrals WHERE paid=1")
    paid_count = c2.fetchone()[0]
    c2.execute("SELECT COUNT(*) FROM referrals WHERE paid=0")
    pending = c2.fetchone()[0]
    c2.execute("SELECT SUM(reward_given) FROM referrals")
    total_rewards = c2.fetchone()[0] or 0
    c2.execute("""SELECT u.username, u.chat_id,
                  COUNT(r.id) as total_r,
                  SUM(CASE WHEN r.paid=1 THEN 1 ELSE 0 END) as paid_r,
                  COALESCE(CAST(u.ref_balance AS INTEGER),0) as bal
                  FROM referrals r JOIN users u ON r.referrer_id=u.chat_id
                  GROUP BY r.referrer_id ORDER BY paid_r DESC LIMIT 10""")
    top = c2.fetchall()
    c2.execute("SELECT COUNT(DISTINCT referrer_id) FROM referrals")
    active_refs = c2.fetchone()[0]
    conn2.close()
    conv_rate = round(paid_count / total * 100, 1) if total > 0 else 0
    lines = [
        "👥 <b>Статистика рефералов</b>\n",
        "Всего переходов: <b>" + str(total) + "</b>",
        "Оплатили: <b>" + str(paid_count) + "</b> (" + str(conv_rate) + "%)",
        "Ожидают оплаты: <b>" + str(pending) + "</b>",
        "Активных рефереров: <b>" + str(active_refs) + "</b>",
        "Выплачено бонусов: <b>" + str(total_rewards) + "⭐</b>\n",
        "🏆 <b>Топ рефереров:</b>"
    ]
    medals = ["🥇","🥈","🥉"] + ["🔸"]*7
    for i, (uname, uid, tot_r, paid_r, bal) in enumerate(top):
        name = ("@" + uname) if uname else ("ID:" + str(uid))
        lines.append(medals[i] + " " + name + " — " + str(paid_r) + "/" + str(tot_r) + " реф. | баланс: " + str(bal) + "⭐")
    b = InlineKeyboardBuilder()
    b.button(text="📋 Рефералы пользователя", callback_data="adm_ref_user")
    b.button(text="⬅️ Назад", callback_data="adm_main")
    b.adjust(1)
    await callback.message.edit_text("\n".join(lines), reply_markup=b.as_markup(),
                                     parse_mode="HTML")

@dp.message(F.document)
async def handle_document_processing(message: types.Message, state: FSMContext):
    try:
        await _doc_inner(message, state)
    except Exception as e:
        logging.exception(f"doc unhandled: {e}")
        try:
            await message.answer("❌ Внутренняя ошибка при обработке файла.")
        except: pass

async def _doc_inner(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    banned_flag, ban_reason = is_banned(user_id)
    if banned_flag:
        await message.answer(f"🚫 Вы заблокированы. Причина: {ban_reason or '—'}"); return

    letters = string.ascii_lowercase
    r = ''.join(random.choice(letters) for _ in range(length))
    caption = message.caption or ''
    file_name = message.document.file_name
    file_format = file_name.rsplit('.', 1)[-1].lower() if '.' in file_name else ''

    sub, message_to_send = await update(user_id, username)
    current_state = await state.get_state()
    if sub:
        await message.answer(message_to_send); return

    is_subscribed, expiry_date_value = await get_user_status_async(user_id)

    allowed, blocked_until = check_antispam(user_id, is_paid=is_subscribed)
    if not allowed:
        secs = max(0, int(blocked_until - time.time()))
        await message.answer(f"🛑 <b>Антиспам:</b> подождите {secs} сек.", parse_mode="HTML"); return

    file_ok, file_blocked_until = check_file_antispam(user_id, is_paid=is_subscribed)
    if not file_ok:
        secs = max(0, int(file_blocked_until - time.time()))
        await message.answer(
            f"🛑 <b>Слишком много файлов!</b> Лимит: {FILE_ANTISPAM_LIMIT} файла за {FILE_ANTISPAM_WINDOW} сек.\n"
            f"Подождите <b>{secs} сек.</b>", parse_mode="HTML"); return

    # ── Batch collection mode ─────────────────────────────────────
    if current_state == BatchFSM.collecting.state:
        file_id_b = message.document.file_id
        file_name_b = message.document.file_name
        added = add_batch_file(user_id, file_id_b, file_name_b)
        if added:
            batch_now = get_batch(user_id)
            cnt_b = len(batch_now.get("files", []))
            await message.answer(
                f"📎 Файл <b>{cnt_b}</b> добавлен: <code>{file_name_b}</code>\n"
                "Отправь ещё или введи <code>/stopbatch</code>",
                parse_mode="HTML")
        else:
            await message.answer("❌ Сначала запусти <code>/batch &lt;команда&gt;</code>", parse_mode="HTML")
        return

    if not is_subscribed:
        not_sub = await check_required_subs(user_id)
        if not_sub:
            await message.answer(
                "🔔 <b>Подпишитесь на каналы для использования бота:</b>\n\n" +
                "\n".join(f"• {ch}" for ch in not_sub) + "\n\nПосле подписки нажмите <b>✅ Проверить</b>",
                reply_markup=kb_check_channels(not_sub), parse_mode="HTML"); return

    if not is_subscribed:
        file_size_mb = (message.document.file_size or 0) / (1024 * 1024)
        if file_size_mb > FREE_MAX_FILE_MB:
            await message.answer(
                f"⚠️ <b>Ограничение бесплатной версии</b>\n\n"
                f"Ваш файл: <b>{file_size_mb:.1f} МБ</b>\nМаксимум для Free: <b>{FREE_MAX_FILE_MB} МБ</b>\n\n"
                f"Купите Premium для работы с большими файлами 👇",
                reply_markup=kb_subscription_plans(), parse_mode="HTML"); return

    inc_msg_count(user_id)

    queue_msg = None
    if is_subscribed:
        await queue_acquire(True)
    else:
        queue_msg = await message.answer("⏳ <b>Ваш запрос в очереди...</b>", parse_mode="HTML")
        await queue_acquire(False)
        if queue_msg:
            try: await queue_msg.delete()
            except: pass

    asyncio.create_task(auto_cleanup())

    _timeout_task: asyncio.Task = None

    async def _file_timeout_watcher():
        if is_subscribed:
            return
        await asyncio.sleep(FREE_TIMEOUT_SEC)
        try:
            await message.answer(
                "⏱ <b>Обработка затянулась!</b>\n\n"
                "Файл обрабатывается дольше обычного.\n"
                "💎 Premium-пользователи не имеют этого ограничения.",
                parse_mode="HTML")
        except Exception:
            pass

    _timeout_task = asyncio.create_task(_file_timeout_watcher())

    try:
        if 'boti' in globals() and 'loging_id' in globals():
            await send_log(message, "файл", f"Формат: {file_format.upper()}")

        if '/color' in caption:
            hex_color, alpha = parse_caption(caption)
            if not hex_color:
                await message.answer("❔ Пример: `/color #FF0000 0.4`", parse_mode='Markdown'); return
            src_dir = Path(f'work/work_COLOR/{r}')
            await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
            download_path = src_dir / file_name
            y = await message.answer(f"<b>⏳ Обрабатываю...</b>", parse_mode="HTML")
            if file_format in ["jpeg", "jpg", "png"]:
                await p_app.download_media(message.document, file_name=download_path)
                processed_bytes = await asyncio.to_thread(_process_image_bytes, download_path, hex_color, alpha)
                bio = io.BytesIO(processed_bytes); bio.name = file_name; bio.seek(0)
                await y.delete()
                await t_client.send_file(message.chat.id, bio, caption='<b>⚡️Файл готов!</b>', parse_mode="HTML", force_document=True)
            elif file_format == "zip":
                await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
                await p_app.download_media(message.document.file_id, file_name=download_path)
                work_dir_parent, output_zip_path = await color_optimized(hex_color, download_path, download_path.stem, alpha)
                await y.delete()
                await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Файл готов!</b>', parse_mode="HTML", force_document=True)
                await asyncio.to_thread(os.remove, output_zip_path)
            else:
                await message.answer(f"❔ Неподдерживаемый формат: .{file_format}")
            if src_dir.exists(): await asyncio.to_thread(shutil.rmtree, src_dir)

        elif '/filters' in caption:
            filter_name, colvo = parse_filter(caption)
            if len(message.caption.split()) < 3:
                await message.answer("❔ Пример: `/filters red` или `/filters light 100`", parse_mode='Markdown'); return
            y = await message.answer(f"<b>⏳ Обрабатываю...</b>", parse_mode="HTML")
            src_dir = Path(f'work/work_COLOR/{r}')
            await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
            download_path = src_dir / file_name
            if file_format in ["jpeg", "jpg", "png"]:
                await p_app.download_media(message.document, file_name=download_path)
                processed_bytes = await asyncio.to_thread(apply_filter_on_bytes_optimized, download_path, filter_name, colvo)
                bio = io.BytesIO(processed_bytes); bio.name = file_name; bio.seek(0)
                await y.delete()
                await t_client.send_file(message.chat.id, bio, caption='<b>⚡️Файл готов!</b>', parse_mode="HTML", force_document=True)
            elif file_format == "zip":
                await p_app.download_media(message.document.file_id, file_name=download_path)
                output_zip_path = await filter_zip(filter_name, download_path, download_path.stem)
                await y.delete()
                await t_client.send_file(message.chat.id, output_zip_path, caption=f'<b>⚡️ZIP с фильтром "{filter_name}" готов!</b>', parse_mode="HTML", force_document=True)
                await asyncio.to_thread(os.remove, download_path)
                await asyncio.to_thread(os.remove, output_zip_path)
                await asyncio.to_thread(shutil.rmtree, src_dir)
            else:
                await message.answer(f"❔ Неподдерживаемый формат: .{file_format}")

        elif '/recolor' in caption:
            recolor_params = parse_recolor_command(caption)
            if not recolor_params:
                await message.answer("❔ Пример: `/recolor #ffbbbb #661717 30`", parse_mode='Markdown'); return
            target_hex, replacement_hex, tolerance = recolor_params
            y = await message.answer(f"<b>⏳ Обрабатываю перекраску...</b>", parse_mode="HTML")
            try:
                if file_format in ["jpeg", "jpg", "png"]:
                    src_dir = Path(f'work/work_COLOR/{r}')
                    await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
                    download_path = src_dir / file_name
                    await p_app.download_media(message.document, download_path)
                    processed_bytes = await asyncio.to_thread(_apply_recolor_to_bytes, download_path, target_hex, replacement_hex, tolerance)
                    if processed_bytes:
                        bio = io.BytesIO(processed_bytes); bio.name = file_name; bio.seek(0)
                        await t_client.send_file(message.chat.id, bio, caption='<b>⚡️Файл готов!</b>', parse_mode="HTML", force_document=True)
                    else:
                        await message.answer("Произошла ошибка при обработке.")
                elif file_format == "zip":
                    download_path = Path(f'work/temp_downloads/src_{r}.zip')
                    await asyncio.to_thread(os.makedirs, download_path.parent, exist_ok=True)
                    await p_app.download_media(message.document.file_id, file_name=download_path)
                    zip_bytes_result = await recolor_zip_optimized(target_hex, replacement_hex, tolerance, download_path)
                    output_zip_path = Path(f'work/temp_downloads/out_{r}.zip')
                    await asyncio.to_thread(output_zip_path.write_bytes, zip_bytes_result)
                    await y.delete()
                    await t_client.send_file(message.chat.id, output_zip_path, caption=f'<b>⚡️ZIP с перекраской готов!</b>', parse_mode="HTML", force_document=True)
                    await asyncio.to_thread(os.remove, download_path)
                    await asyncio.to_thread(os.remove, output_zip_path)
                else:
                    await message.answer(f"❔ Неподдерживаемый формат: .{file_format}")
            except Exception as e:
                await message.answer(f"Непредвиденная ошибка: {e}")
            finally:
                try: await y.delete()
                except: pass

        elif '/quality' in caption:
            level = parse_quality(caption)
            if not level:
                await message.answer("❔ Пример: `/quality 16`", parse_mode='Markdown'); return
            processing_message = await message.answer("Обрабатываю...")
            try:
                if file_format in ["jpeg", "jpg", "png"]:
                    src_dir = Path(f'work/work_COLOR/{r}')
                    await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
                    download_path = src_dir / file_name
                    await p_app.download_media(message.document, file_name=download_path)
                    processed_bytes = await asyncio.to_thread(quality_func, download_path, level)
                    bio = io.BytesIO(processed_bytes); bio.name = file_name; bio.seek(0)
                    await t_client.send_file(message.chat.id, bio, caption='<b>⚡️Файл готов!</b>', parse_mode="HTML", force_document=True)
                elif file_format == "zip":
                    download_path = Path(f'work/temp_downloads/src_{r}.zip')
                    await asyncio.to_thread(os.makedirs, download_path.parent, exist_ok=True)
                    await p_app.download_media(message.document.file_id, file_name=download_path)
                    zip_bytes_result = await quality_zip(level, download_path)
                    output_zip_path = Path(f'work/temp_downloads/out_{r}.zip')
                    await asyncio.to_thread(output_zip_path.write_bytes, zip_bytes_result)
                    await processing_message.delete()
                    await t_client.send_file(message.chat.id, output_zip_path, caption=f'<b>⚡️ZIP с качеством готов!</b>', parse_mode="HTML", force_document=True)
                    await asyncio.to_thread(os.remove, download_path)
                    await asyncio.to_thread(os.remove, output_zip_path)
                else:
                    await message.answer(f"❔ Неподдерживаемый формат: .{file_format}")
            except Exception as e:
                await message.answer(f"Непредвиденная ошибка: {e}")
            finally:
                try: await processing_message.delete()
                except: pass

        elif '/aim' in caption:
            if file_format not in ["png", "jpg", "jpeg"]:
                await message.answer(f"❔ Неподдерживаемый формат: .{file_format}"); return
            processing_message = await message.answer("Обрабатываю...")
            try:
                src_dir = Path(f'work/work_COLOR/{r}')
                await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
                download_path = src_dir / file_name
                await p_app.download_media(message.document, file_name=download_path)
                processed_bytes = await asyncio.to_thread(process_aim_image_optimized, download_path)
                bio = io.BytesIO(processed_bytes); bio.name = f"aim_{file_name}"
                await t_client.send_file(message.chat.id, bio, caption=f'<b>⚡️Прицел готов!</b>', parse_mode="HTML", force_document=True)
            except Exception as e:
                await message.answer(f"Ошибка: {e}")
            finally:
                await processing_message.delete()

        elif '/compress' in caption:
            width, height = parse_caption_for_compression(caption)
            if not width:
                await message.answer("Ошибка парсинга размера."); return
            target_size = (width, height)
            processing_message = await message.answer(f"Обрабатываю сжатие до {width}x{height}...")
            src_dir = Path(f'work/work_COMPRESS/{r}')
            await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
            download_path = src_dir / file_name
            if file_format in ["jpeg", "jpg", "png"]:
                await p_app.download_media(message.document, file_name=download_path)
                processed_bytes, new_format = await asyncio.to_thread(_compress_image_bytes_sync, download_path, target_size, file_format)
                bio = io.BytesIO(processed_bytes); bio.name = f"compressed_{Path(file_name).stem}.{new_format}"
                await processing_message.delete()
                await t_client.send_file(message.chat.id, bio, caption='<b>⚡️Файл готов!</b>', parse_mode="HTML", force_document=True)
            elif file_format == "zip":
                await p_app.download_media(message.document.file_id, destination=download_path)
                output_zip_path = src_dir / f"{download_path.stem}_compressed.zip"
                await asyncio.to_thread(_process_zip_sync, download_path, output_zip_path, target_size)
                await processing_message.delete()
                await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Файл готов!</b>', parse_mode="HTML", force_document=True)
            else:
                await processing_message.delete()
                await message.answer(f"❔ Неподдерживаемый формат: .{file_format}")
            if src_dir.exists(): await asyncio.to_thread(shutil.rmtree, src_dir)

        elif '/logo' in caption:
            n = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            work_dir = Path(f'work/work_LOGO/{r}')
            await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
            src = os.path.join(work_dir, file_name)
            download_path = work_dir / file_name
            try:
                await p_app.download_media(message.document.file_id, file_name=download_path)
                y = await message.answer("Обрабатываю...")
                success, zip_path = await asyncio.get_running_loop().run_in_executor(None, create_and_zip_files, src, work_dir, n, file_format, "logo", FILE_SUFFIXES)
                await y.delete()
                await t_client.send_file(message.chat.id, zip_path, caption=f'<b>⚡️Ваши логотипы готовы!</b>', parse_mode='HTML')
            except Exception as e: await message.answer(f"Ошибка: {e}")
            finally:
                if os.path.exists(work_dir): shutil.rmtree(work_dir)

        elif '/tree' in caption:
            n = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            work_dir = Path(f'work/work_TREE/{r}')
            await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
            src = os.path.join(work_dir, file_name)
            download_path = work_dir / file_name
            try:
                await p_app.download_media(message.document.file_id, file_name=download_path)
                y = await message.answer("Обрабатываю...")
                success, zip_path = await asyncio.get_running_loop().run_in_executor(None, create_and_zip_files, src, work_dir, n, file_format, "tree", Tree)
                await y.delete()
                await t_client.send_file(message.chat.id, zip_path, caption=f'<b>⚡️Ваши деревья готовы!</b>', parse_mode="HTML", force_document=True)
            except Exception as e: await message.answer(f"Ошибка: {e}")
            finally:
                if os.path.exists(work_dir): shutil.rmtree(work_dir)

        elif '/bild' in caption:
            n = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            work_dir = Path(f'work/work_BILD/{r}')
            await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
            src = os.path.join(work_dir, file_name)
            download_path = work_dir / file_name
            try:
                await p_app.download_media(message.document.file_id, file_name=download_path)
                y = await message.answer("Обрабатываю...")
                success, zip_path = await asyncio.get_running_loop().run_in_executor(None, create_and_zip_files, src, work_dir, n, file_format, "bild", bild)
                await y.delete()
                await t_client.send_file(message.chat.id, zip_path, caption=f'<b>⚡️Ваши билдборды готовы!</b>', parse_mode="HTML", force_document=True)
            except Exception as e: await message.answer(f"Ошибка: {e}")
            finally:
                if os.path.exists(work_dir): shutil.rmtree(work_dir)

        elif '/map' in caption:
            if file_format in ["jpeg", "jpg", "png"]:
                y = await message.answer("Обрабатываю...")
                src_dir = Path(f'work/work_MAP/{r}')
                src_dir.mkdir(parents=True, exist_ok=True)
                file_path = src_dir / file_name
                await p_app.download_media(message.document, file_name=str(file_path.absolute()))
                img = Image.open(str(file_path.absolute()))
                width, height = img.size
                num_squares_side = 14
                square_width = width // num_squares_side
                square_height = height // num_squares_side
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
                    for i in range(num_squares_side):
                        for j_idx in range(num_squares_side):
                            box = (j_idx*square_width, i*square_height, (j_idx+1)*square_width, (i+1)*square_height)
                            square = img.crop(box)
                            square_buffer = io.BytesIO()
                            save_format = 'JPEG' if file_format in ['jpeg','jpg'] else 'PNG'
                            square.save(square_buffer, format=save_format)
                            square_buffer.seek(0)
                            archive.writestr(f"radar{str(i*num_squares_side+j_idx).zfill(2)}.{save_format.lower()}", square_buffer.getvalue())
                zip_buffer.seek(0); zip_buffer.name = f'{r}_radar.zip'
                await y.delete()
                await t_client.send_file(message.chat.id, zip_buffer, caption=f'<b>⚡️Ваша карта готова!</b>', parse_mode='HTML')

        elif '/remap' in caption:
            if not message.document.file_name.lower().endswith('.zip'):
                await message.answer("Пожалуйста, загрузите .zip файл."); return
            y = await message.answer("Восстанавливаю изображение...")
            work_dir = Path(f'work/work_MAP/{r}')
            await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
            download_path = work_dir / file_name
            await p_app.download_media(message.document.file_id, file_name=download_path)
            images_dict = {}
            num_squares_side = 14
            total_squares = num_squares_side * num_squares_side
            with zipfile.ZipFile(download_path, 'r') as archive:
                for zipinfo in archive.infolist():
                    fn = zipinfo.filename
                    if fn.startswith('radar') and (fn.endswith('.jpg') or fn.endswith('.jpeg') or fn.endswith('.png')):
                        index = int(fn[5:-4].replace(".",""))
                        with archive.open(zipinfo) as fiz: images_dict[index] = Image.open(io.BytesIO(fiz.read()))
            if len(images_dict) != total_squares:
                await y.delete(); await message.answer(f"Найдено только {len(images_dict)} из {total_squares} частей."); return
            first_image = next(iter(images_dict.values()))
            sq_w, sq_h = first_image.size
            restored_img = Image.new('RGBA', (sq_w * num_squares_side, sq_h * num_squares_side))
            for idx in range(total_squares):
                i, j_idx = idx // num_squares_side, idx % num_squares_side
                restored_img.paste(images_dict[idx], (j_idx*sq_w, i*sq_h))
            jjj = f'work/work_MAP/{r}/restored_radar.png'
            restored_img.save(jjj, format='PNG', quality=95)
            await y.delete()
            await t_client.send_file(message.chat.id, jjj, caption=f'<b>⚡️Восстановленное изображение готово!</b>', parse_mode=enums.ParseMode.HTML, force_document=True)

        elif '/hudcut' in caption:
            if file_format not in ["png", "jpg", "jpeg"]:
                await message.answer(f"❔ Неподдерживаемый формат: .{file_format}"); return
            processing_message = await message.answer("Обрабатываю...")
            try:
                src_dir = Path(f'work/work_HUD/{r}')
                await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
                download_path = src_dir / file_name
                await p_app.download_media(message.document, download_path)
                zip_buffer, count = await asyncio.to_thread(process_image_sync, download_path)
                zip_buffer.seek(0); zip_buffer.name = f'{r}_hudcut.zip'
                await t_client.send_file(message.chat.id, zip_buffer, caption=f'<b>⚡️Нарезаный худ готов!</b>', parse_mode="HTML", force_document=True)
            except Exception as e: logging.exception("Ошибка hudcut")
            finally: await processing_message.delete()

        elif '/rehud' in caption:
            if not message.document.file_name.lower().endswith('.zip'):
                await message.answer("Пожалуйста, загрузите .zip файл."); return
            y = await message.answer("Восстанавливаю изображение...")
            work_dir = Path(f'work/work_HUD/{r}')
            await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
            download_path = work_dir / file_name
            await p_app.download_media(message.document.file_id, file_name=download_path)
            await asyncio.to_thread(assemble_image_from_zip_bytes, download_path, f'work/work_HUD/{r}/rehud_{r}.png')
            await y.delete()
            await t_client.send_file(message.chat.id, f'work/work_HUD/{r}/rehud_{r}.png', caption=f'<b>⚡️Восстановленное изображение готово!</b>', parse_mode=enums.ParseMode.HTML, force_document=True)

        elif '/genrl' in caption:
            work_dir = Path(f'work/work_BPC/{r}')
            work_dir.mkdir(parents=True, exist_ok=True)
            y = await message.answer("<b>⏳ Обрабатываю...</b>", parse_mode="HTML")
            download_path = work_dir / file_name
            bpcmeta_path = work_dir / f'{r}_GENERIC.bpcmeta'
            try:
                await p_app.download_media(message.document.file_id, file_name=str(download_path))
                genrl_target = str(download_path)
                if not zipfile.is_zipfile(str(download_path)):
                    raw = read_file_bytes(str(download_path))
                    xor_key = detect_key_pattern(raw)
                    dec = bytearray(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(raw))
                    dec_path = work_dir / (Path(file_name).stem + '_dec.zip')
                    dec_path.write_bytes(bytes(dec))
                    if not zipfile.is_zipfile(str(dec_path)): raise ValueError("Файл не является zip-архивом.")
                    genrl_target = str(dec_path)
                generate_bpcmeta(genrl_target, str(bpcmeta_path))
                await y.delete()
                await t_client.send_file(message.chat.id, str(bpcmeta_path), caption='<b>⚡️Твой генрл готов!</b>', parse_mode='html', force_document=True)
            except Exception as e: await y.edit_text(f"<b>❌ Ошибка: {e}</b>", parse_mode="HTML")
            finally: shutil.rmtree(work_dir, ignore_errors=True)
            return

        elif "/bpc" in caption:
            file_name = message.document.file_name
            temp_dir = os.path.join(f"work/work_BPC/{r}")
            os.makedirs(temp_dir, exist_ok=True)
            await p_app.download_media(message.document.file_id, file_name=f'work/work_BPC/{r}/{file_name}')
            await process_zip_file(file_name, message, r, temp_dir)
            return

        elif "/nri" in caption:
            y = await message.answer(f"<b>⏳ Обрабатываю...</b>", parse_mode="HTML", force_document=True)
            file_name = message.document.file_name
            temp_dir = f"work/work_Z2N/{r}"
            os.makedirs(temp_dir, exist_ok=True)
            await p_app.download_media(message.document.file_id, file_name=f'work/work_Z2N/{r}/{file_name}')
            i_result = convert_zip2nonerai(f'work/work_Z2N/{r}/{file_name}', temp_dir)
            await y.delete()
            await t_client.send_file(message.chat.id, i_result, caption='<b>⚡️Твоя сборка готова!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(temp_dir)
            return

        elif '/merger' in caption:
            parts = caption.split()
            if len(parts) < 2:
                await message.answer("❔ Формат: /merger <имя_текстуры>"); return
            target_name = parts[1]
            if file_format not in ('zip', 'bpc'):
                await message.answer("❔ Загрузите .zip или .bpc архив."); return
            y = await message.answer("⏳<b>Обрабатываю...</b>", parse_mode="HTML")
            work_dir = Path(f'work/work_BPC/{r}')
            work_dir.mkdir(parents=True, exist_ok=True)
            download_path = work_dir / file_name
            try:
                await p_app.download_media(message.document.file_id, file_name=download_path)
                raw = read_file_bytes(str(download_path))
                if file_format == 'bpc':
                    xor_key = detect_key_pattern(raw)
                    raw = bytearray(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(raw))
                with zipfile.ZipFile(io.BytesIO(bytes(raw)), 'r') as zf:
                    names_in_zip = [Path(n).stem for n in zf.namelist() if not n.endswith('/') and not n.startswith('__MACOSX')]
                merger_data = {target_name: names_in_zip}
                merger_path = work_dir / f'Merger_{r}.json'
                with open(merger_path, 'w', encoding='utf-8') as f: json.dump(merger_data, f, indent=4, ensure_ascii=False)
                await y.delete()
                await t_client.send_file(message.chat.id, str(merger_path), caption=f'<b>⚡️Merger.json готов!</b>\n📄 Файлов: {len(names_in_zip)}', parse_mode="HTML", force_document=True)
            except Exception as e: await y.edit_text(f"<b>❌ Ошибка: {e}</b>", parse_mode="HTML")
            finally: shutil.rmtree(work_dir, ignore_errors=True)
            return

        elif '/index' in caption:
            y = await message.answer("⏳<b>Индексирую...</b>", parse_mode="HTML")
            work_dir = Path(f'work/work_BPC/{r}')
            work_dir.mkdir(parents=True, exist_ok=True)
            download_path = work_dir / file_name
            try:
                await p_app.download_media(message.document.file_id, file_name=download_path)
                raw = read_file_bytes(str(download_path))
                out_zip_buf = io.BytesIO()
                with zipfile.ZipFile(io.BytesIO(bytes(raw)), 'r') as zf_in:
                    with zipfile.ZipFile(out_zip_buf, 'w', zipfile.ZIP_STORED) as zf_out:
                        for info in zf_in.infolist():
                            if info.is_dir() or info.filename.startswith('__MACOSX'): continue
                            data = zf_in.read(info.filename)
                            zf_out.writestr(info.filename, data[:136])
                out_zip_buf.seek(0)
                out_name = Path(file_name).stem + '.tmb'
                out_zip_buf.name = out_name
                await y.delete()
                await t_client.send_file(message.chat.id, out_zip_buf, caption=f'<b>⚡️Индекс готов!</b>\n📦 {out_name}', parse_mode="HTML", force_document=True)
            except Exception as e: await y.edit_text(f"<b>❌ Ошибка: {e}</b>", parse_mode="HTML")
            finally: shutil.rmtree(work_dir, ignore_errors=True)
            return

        elif '/ptk' in caption:
            y = await message.answer(f"<b>⏳ Обрабатываю...</b>", parse_mode="HTML")
            work_dir = Path(f'work/work_COLOR/{r}')
            await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
            download_path = work_dir / file_name
            await p_app.download_media(message.document.file_id, file_name=download_path)
            o = await create_palette_image(str(download_path), file_name, n_colors=10, output_file=str(work_dir / 'palette.png'))
            await y.delete()
            await t_client.send_file(message.chat.id, str(work_dir / 'palette.png'), caption=f'<b>⚡️{o}</b>', parse_mode="HTML")
            shutil.rmtree(work_dir)
            return

        elif '/overlay' in caption:
            if len(message.caption.split()) < 3:
                await message.answer("❔ Формат: /overlay <mode> <alpha>\n\nМоды: multiply, screen, overlay, add, darker"); return
            parts = caption.split()
            mode = parts[1] if len(parts) > 1 else "normal"
            alpha = int(parts[2]) if len(parts) > 2 else 100
            if file_format not in ["jpeg", "jpg", "png", "zip"]:
                return await message.answer("❌ Поддерживаются только изображения или архив!")
            src_dir = Path(f'work/work_OVERLAY/{r}')
            os.makedirs(src_dir, exist_ok=True)
            download_path = src_dir / file_name
            await p_app.download_media(message.document, file_name=str(download_path))
            await state.update_data(base_path=str(download_path), mode=mode, alpha=alpha, original_name=file_name)
            await state.set_state(OverlayStates.waiting_for_second_image)
            await message.answer(f"<b>✅ Первый файл получен!</b>\nРежим: <code>{mode}</code>\nПрозрачность: <code>{alpha}%</code>\n\nТеперь пришли <b>второй файл</b>.", parse_mode="HTML")
            return

        if current_state == OverlayStates.waiting_for_second_image:
            second_ext = file_name.split('.')[-1].lower()
            second_path = Path(f"work/work_OVERLAY/overlay_src_{r}.{second_ext}")
            data = await state.get_data()
            y = await message.answer(f"<b>⏳ Начинаю обработку...</b>", parse_mode="HTML")
            await p_app.download_media(message.document, file_name=str(second_path))
            if data['original_name'].lower().endswith('.zip'):
                result_buffer = await asyncio.to_thread(_process_zip_overlay, data['base_path'], str(second_path), data['mode'], data['alpha'])
                out_filename = f"processed_{r}.zip"
            else:
                processed_bytes = await asyncio.to_thread(_process_overlay_logic, data['base_path'], str(second_path), data['mode'], data['alpha'])
                result_buffer = io.BytesIO(processed_bytes)
                out_filename = f"result_{data['original_name']}"
            result_buffer.name = out_filename; result_buffer.seek(0)
            await t_client.send_file(message.chat.id, result_buffer, caption='<b>⚡️ Готово!</b>', parse_mode="HTML", force_document=True)
            await y.delete(); await state.clear()
            return

        else:
            if file_format == "ifp":
                src_dir = Path(f'work/work_ANI/{r}')
                os.makedirs(src_dir, exist_ok=True)
                download_path = src_dir / file_name
                await p_app.download_media(message.document, download_path)
                file_name2 = file_name.split(".")[0]
                ani_file_path = f'work/work_ANI/{r}/{file_name2}.ani'
                y = await message.answer("Обрабатываю...")
                with open(download_path, 'rb') as f_input, open(ani_file_path, 'wb') as f_output:
                    f_input.seek(8)
                    byte = f_input.read(8)
                    while byte: f_output.write(byte); byte = f_input.read(8)
                async with aiofiles.open(ani_file_path, "rb") as f: original_data = await f.read()
                new_data = b'\x41\x4E\x50\x33' + original_data
                with open(ani_file_path, 'wb') as er: er.write(new_data)
                await y.delete()
                await t_client.send_file(message.chat.id, f'work/work_ANI/{r}/{file_name2}.ani', caption=f'<b>⚡️Ваша анимация готова!</b>', parse_mode="HTML", force_document=True)
                try: os.removedirs(f'work/work_ANI/{r}')
                except: pass

            elif file_format == "json":
                work_dir = Path(f'work/temp_downloads/{r}')
                await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
                src = os.path.join(work_dir, file_name)
                download_path = work_dir / file_name
                try:
                    await p_app.download_media(message.document.file_id, file_name=download_path)
                    y = await message.answer("Обрабатываю...")
                    i_result = await asyncio.get_running_loop().run_in_executor(None, process_json_file, src)
                    await y.delete()
                    await message.answer(str(i_result))
                except Exception as e: await message.answer(f"Ошибка: {e}")
                finally:
                    if os.path.exists(work_dir): shutil.rmtree(work_dir)

            elif file_format == "cls":
                src_dir = Path(f'work/work_COL/{r}')
                os.makedirs(src_dir, exist_ok=True)
                download_path = src_dir / file_name
                await p_app.download_media(message.document, download_path)
                file_name2 = file_name.split(".")[0]
                ani_file_path = f'work/work_COL/{r}/{file_name2}.col'
                y = await message.answer("Обрабатываю...")
                with open(download_path, 'rb') as f_input, open(ani_file_path, 'wb') as f_output:
                    f_input.seek(4)
                    byte = f_input.read(4)
                    while byte: f_output.write(byte); byte = f_input.read(4)
                async with aiofiles.open(ani_file_path, "rb") as f: original_data = await f.read()
                new_data = b'\x43\x4F\x4C\x33' + original_data
                with open(ani_file_path, 'wb') as er: er.write(new_data)
                await y.delete()
                await t_client.send_file(message.chat.id, ani_file_path, caption='Держи файл!')
                try: os.removedirs(f'work/work_COL/{r}')
                except: pass

            elif file_format == "bpc":
                await send_log(message, "файл", "Обработка BPC")
                file_name = message.document.file_name
                temp_dir = os.path.join(f"work/work_BPC/{r}")
                os.makedirs(temp_dir, exist_ok=True)
                await p_app.download_media(message.document.file_id, file_name=f'work/work_BPC/{r}/{file_name}')
                await process_bpc_file(file_name, message, r, temp_dir)

            elif file_format == "txd":
                txd_converter = TXDConverter()
                y = await message.answer(f"<b>⏳ Обрабатываю...</b>", parse_mode="HTML")
                try:
                    src_dir = Path(f'work/work_COL/{r}')
                    os.makedirs(src_dir, exist_ok=True)
                    download_path = src_dir / file_name
                    await p_app.download_media(message.document, download_path)
                    with open(download_path, 'rb') as f: data = f.read()
                    png_files = txd_converter.parse_txd_data(data)
                    if not png_files:
                        await y.edit_text("<b>Не удалось извлечь текстуры</b>"); return
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for png_file in png_files: zip_file.write(png_file, os.path.basename(png_file))
                    zip_buffer.seek(0)
                    bio = io.BytesIO(zip_buffer.getvalue()); bio.name = f"{Path(message.document.file_name).stem}.zip"
                    await t_client.send_file(message.chat.id, bio, caption=f'<b>⚡️Ваши файлы готовы!</b>', parse_mode="HTML", force_document=True)
                except Exception as e: logging.error(f"TXD processing error: {e}", exc_info=True)
                finally: await y.delete()

            elif file_format == "mod":
                y = await message.answer(f"<b>⏳ Обрабатываю...</b>", parse_mode="HTML")
                file_name = message.document.file_name
                file_name2 = file_name.split(".")[0]
                download_path = Path(f'work/work_MOD/{r}')
                file_down = f'work/work_MOD/{r}/{file_name}'
                os.makedirs(download_path, exist_ok=True)
                await p_app.download_media(message.document.file_id, file_name=file_down)
                await convert_one(file_down, str(download_path))
                await y.delete()
                await t_client.send_file(message.chat.id, f'work/work_MOD/{r}/{file_name2}.dff', caption=f'<b>⚡️Ваша модель готова!</b>', parse_mode="HTML", force_document=True)

            elif file_format in ["btx", "png", "jpg", "jpeg", "zip"]:
                work_dir = Path(f'work/work_BTX/{r}')
                file_name = message.document.file_name
                file_name2 = Path(file_name).stem
                os.makedirs(work_dir, exist_ok=True)
                src_path = work_dir / file_name
                s = btx_user_settings.get(user_id, {})
                bw, bh = s.get("block", BTX_DEFAULT_BLOCK)
                quality = s.get("quality", BTX_DEFAULT_QUALITY)
                await send_log(message, "файл", f"Формат: {file_format.upper()} | ASTC {bw}x{bh} | quality={quality}")
                y = await message.answer(f"<b>⏳ Обрабатываю {file_format.upper()}...</b>", parse_mode="HTML")
                try:
                    await p_app.download_media(message.document, file_name=src_path)
                    if file_format == "btx":
                        out_png = await convert_btx_to_png(src_path, file_name, work_dir)
                        if out_png and out_png.exists():
                            await y.delete()
                            await t_client.send_file(message.chat.id, str(out_png), caption=f'<b>⚡️{file_name2}.png готов!</b>', parse_mode="HTML", force_document=True)
                        else:
                            await y.edit_text("<b>Не удалось конвертировать BTX → PNG</b>", parse_mode="HTML")
                    elif file_format in ["png", "jpg", "jpeg"]:
                        out_btx = await convert_png_to_btx(src_path, file_name, work_dir, bw, bh, quality)
                        if out_btx and out_btx.exists():
                            await y.delete()
                            await t_client.send_file(message.chat.id, str(out_btx), caption=f'<b>⚡️{file_name2}.btx готов!</b>\n🔷 Блок: {bw}x{bh} | ⚙️ Качество: {s.get("quality_name","medium")}', parse_mode="HTML", force_document=True)
                        else:
                            await y.edit_text("<b>Не удалось конвертировать PNG → BTX</b>", parse_mode="HTML")
                    elif file_format == "zip":
                        out_btx_dir = work_dir / "btx_out"
                        out_btx_dir.mkdir(exist_ok=True)
                        out_zip_path = work_dir / f"{file_name2}_btx.zip"
                        with zipfile.ZipFile(src_path, 'r') as src_zip:
                            png_list = [n for n in src_zip.namelist() if n.lower().endswith(('.png','.jpg','.jpeg'))]
                        converted_count = 0
                        with zipfile.ZipFile(out_zip_path, 'w', zipfile.ZIP_STORED) as out_zip:
                            with zipfile.ZipFile(src_path, 'r') as src_zip:
                                for fname in src_zip.namelist():
                                    if fname.lower().endswith(('.png','.jpg','.jpeg')):
                                        img_bytes = src_zip.read(fname)
                                        img = Image.open(io.BytesIO(img_bytes))
                                        btx_bytes = await asyncio.to_thread(_compress_to_btx_bytes, img, bw, bh, quality)
                                        stem = Path(fname).stem
                                        out_zip.writestr(stem + '.btx', btx_bytes)
                                        converted_count += 1
                                    elif fname.lower().endswith('.btx'):
                                        raw = src_zip.read(fname)
                                        img = await asyncio.to_thread(_decompress_from_btx_bytes, raw)
                                        buf = io.BytesIO(); img.save(buf, format='PNG')
                                        out_zip.writestr(Path(fname).stem + '.png', buf.getvalue())
                                        converted_count += 1
                                    else:
                                        out_zip.writestr(fname, src_zip.read(fname))
                        await y.delete()
                        await t_client.send_file(message.chat.id, str(out_zip_path), caption=(
                            f'<b>⚡️ZIP конвертирован!</b>\n🔄 Файлов обработано: {converted_count}\n'
                            f'🔷 Блок: {bw}x{bh} | ⚙️ Качество: {s.get("quality_name","medium")}'), parse_mode="HTML", force_document=True)
                except Exception as e:
                    logging.error(f"BTX handler error: {e}", exc_info=True)
                    await y.edit_text("❌ Произошла ошибка при обработке файла")

            elif file_format == "dat":
                y = await message.answer(f"<b>⏳ Обрабатываю...</b>", parse_mode="HTML")
                try:
                    file_name = message.document.file_name
                    file_name2 = file_name.split(".")[0]
                    temp = f'work/work_MOD/{r}'
                    os.makedirs(temp, exist_ok=True)
                    await p_app.download_media(message.document.file_id, file_name=temp)
                    json_file_path = f'work/work_MOD/{r}/{file_name2}.json'
                    json_result = await convert_timecyc_dat_to_json(json_file_path, file_name, temp)
                    await t_client.send_file(message.chat.id, json_file_path, caption=f'<b>⚡️Ваш файл готов!</b>', parse_mode="HTML", force_document=True)
                except Exception as e: logging.error(f"DAT processing error: {e}", exc_info=True)
                finally: await y.delete()

    finally:
        if _timeout_task and not _timeout_task.done():
            _timeout_task.cancel()
        await queue_release(is_subscribed)

@dp.message(F.photo)
async def handle_photo(message: types.Message): await send_log(message, "фото")

@dp.message(F.sticker)
async def handle_sticker(message: types.Message): await send_log(message, "стикер")

@dp.message(F.animation)
async def handle_animation(message: types.Message): await send_log(message, "гифка")

@dp.message(F.video)
async def handle_video(message: types.Message): await send_log(message, "видео")

@dp.message(F.voice)
async def handle_voice(message: types.Message): await send_log(message, "голосовое")

@dp.message(F.audio)
async def handle_audio(message: types.Message): await send_log(message, "аудио")

@dp.message(F.video_note)
async def handle_video_note(message: types.Message): await send_log(message, "видео-сообщение")

@dp.message(F.contact)
async def handle_contact(message: types.Message): await send_log(message, "контакт")

@dp.message(F.location)
async def handle_location(message: types.Message): await send_log(message, "геолокация")

@dp.message(F.poll)
async def handle_poll(message: types.Message): await send_log(message, "опрос", f"Вопрос: {message.poll.question}")

@dp.message(F.story)
async def handle_story(message: types.Message): await send_log(message, "история")

@dp.message(F.text)
async def ok(message: types.Message):
    try:
        await _ok_inner(message)
    except Exception as e:
        logging.exception(f"ok unhandled: {e}")
        try:
            await message.answer("❌ Внутренняя ошибка. Попробуйте ещё раз.")
        except: pass

async def _ok_inner(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    banned_flag, ban_reason = is_banned(user_id)
    if banned_flag:
        await message.answer(f"🚫 Вы заблокированы. Причина: {ban_reason or '—'}"); return

    sub, message_to_send = await update(user_id, username)
    if sub:
        await message.answer(message_to_send); return

    is_subscribed, expiry_date_value = await get_user_status_async(user_id)

    allowed, blocked_until = check_antispam(user_id, is_paid=is_subscribed)
    if not allowed:
        secs = max(0, int(blocked_until - time.time()))
        await message.answer(f"🛑 <b>Антиспам:</b> подождите {secs} сек.", parse_mode="HTML"); return

    try:
        await send_log(message, "текст")
    except Exception as e:
        logging.warning(f"send_log: {e}")

    inc_msg_count(user_id)

    j = message.text.split()

    if "/start" in message.text:
        if is_subscribed:
            b = InlineKeyboardBuilder()
            b.button(text="🔧 Открыть палитру HEX", web_app=types.WebAppInfo(url="https://csscolor.ru"))
            await message.answer(start_paid_text(expiry_date_value or "—"), reply_markup=b.as_markup(), parse_mode='HTML')
        else:
            ref_disc = get_buyer_discount(user_id)
            if ref_disc > 0:
                await message.answer(
                    "👥 <b>Вас пригласил друг!</b> Скидка <b>-" + str(ref_disc) + "%</b> уже применена к тарифам 🎉",
                    parse_mode="HTML")
            if can_use_trial(user_id):
                b_trial = InlineKeyboardBuilder()
                b_trial.button(text="⚡ Попробовать 3 дня за 1⭐", callback_data="buy_trial")
                b_trial.button(text="💎 Посмотреть тарифы", callback_data="show_plans")
                b_trial.adjust(1)
                await message.answer(
                    "👋 <b>Добро пожаловать в " + BOT_NAME + "!</b>\n\n"
                    "🎁 <b>Специальное предложение для новых пользователей:</b>\n"
                    "3 дня Premium всего за <b>1⭐</b>\n\n"
                    "После пробного периода выберете удобный тариф.",
                    reply_markup=b_trial.as_markup(), parse_mode="HTML")
            else:
                await message.answer(start_free_text(), reply_markup=kb_subscription_plans(), parse_mode='HTML')
        return

    if "/mysub" in message.text:
        if is_subscribed:
            forever = expiry_date_value == "31.12.2099"
            until = "♾️ бессрочно" if forever else f"до <b>{expiry_date_value}</b>"
            await message.answer(f"💎 <b>Premium активен</b> — {until}", parse_mode="HTML")
        else:
            await message.answer("❌ <b>У вас нет Premium-подписки</b>\n\nКупить: /start", reply_markup=kb_subscription_plans(), parse_mode="HTML")
        return

    if "/top" in message.text:
        rows = get_top_users(10)
        medals = ["🥇","🥈","🥉"]+["🔸"]*7
        lines = ["🏆 <b>Топ-10 активных пользователей:</b>\n"]
        for i, (uid, uname, cnt) in enumerate(rows):
            name = f"@{uname}" if uname else f"ID:{uid}"
            lines.append(f"{medals[i]} {i+1}. {name} — <b>{cnt}</b> действий")
        await message.answer("\n".join(lines), parse_mode="HTML"); return

    if "/admin" in message.text:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT admin FROM users WHERE chat_id=?", (user_id,))
        row = c.fetchone(); conn.close()
        if not (row and row[0] == 'True'):
            await message.answer("❌ Нет прав."); return
        s = get_bot_stats()
        role_label = ROLES.get(get_role(user_id), {}).get("label", "👤 Стафф")
        text = (f"🛠 <b>Панель {role_label}</b>\n\n"
                f"👥 Всего пользователей: <b>{s['total']}</b>\n"
                f"💎 Premium: <b>{s['paid']}</b>\n"
                f"🆓 Бесплатных: <b>{s['free']}</b>\n"
                f"🚫 Заблокировано: <b>{s['banned']}</b>\n"
                f"📅 Активно сегодня: <b>{s['today']}</b>\n"
                f"💾 Work-папка: <b>{get_work_size_gb():.2f} ГБ</b>")
        await message.answer(text, reply_markup=kb_admin_main(user_id), parse_mode="HTML"); return

    if message.text.startswith("/addchannel"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT admin FROM users WHERE chat_id=?", (user_id,))
        row = c.fetchone(); conn.close()
        if not (row and row[0] == 'True'):
            await message.answer("❌ Нет прав."); return
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("Использование: /addchannel @username"); return
        ch = parts[1] if parts[1].startswith("@") else "@" + parts[1]
        add_channel(ch)
        await message.answer(f"✅ Канал {ch} добавлен в обязательные."); return

    if message.text.startswith("/delchannel"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT admin FROM users WHERE chat_id=?", (user_id,))
        row = c.fetchone(); conn.close()
        if not (row and row[0] == 'True'):
            await message.answer("❌ Нет прав."); return
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("Использование: /delchannel @username"); return
        ch = parts[1] if parts[1].startswith("@") else "@" + parts[1]
        ok_del = remove_channel(ch)
        await message.answer(f"{'✅ Удалён' if ok_del else '❌ Не найден'}: {ch}"); return

    if message.text.startswith("/ban "):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT admin FROM users WHERE chat_id=?", (user_id,))
        row = c.fetchone(); conn.close()
        if not (row and row[0] == 'True'):
            await message.answer("❌ Нет прав."); return
        parts = message.text.split(maxsplit=2)
        try:
            uid = int(parts[1])
            reason = parts[2] if len(parts) > 2 else "Нарушение правил"
            ban_user(uid, reason)
            await message.answer(f"🚫 Пользователь <code>{uid}</code> заблокирован.\nПричина: {reason}", parse_mode="HTML")
        except (ValueError, IndexError): await message.answer("❌ Неверный ID")
        return

    if message.text.startswith("/unban "):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT admin FROM users WHERE chat_id=?", (user_id,))
        row = c.fetchone(); conn.close()
        if not (row and row[0] == 'True'):
            await message.answer("❌ Нет прав."); return
        parts = message.text.split()
        try:
            uid = int(parts[1])
            unban_user(uid)
            await message.answer(f"✅ Пользователь <code>{uid}</code> разбанен.", parse_mode="HTML")
        except (ValueError, IndexError): await message.answer("❌ Неверный ID")
        return

    if message.text.startswith("/givesub"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT admin FROM users WHERE chat_id=?", (user_id,))
        row = c.fetchone(); conn.close()
        if not (row and row[0] == 'True'):
            await message.answer("❌ Нет прав."); return
        parts = message.text.split()
        if len(parts) < 3:
            await message.answer("Использование: /givesub <id> <days>\n-1 = навсегда"); return
        try:
            uid = int(parts[1]); days = int(parts[2])
            expiry = grant_subscription(uid, days)
            await message.answer(f"✅ Подписка выдана <code>{uid}</code> до <b>{expiry}</b>", parse_mode="HTML")
        except ValueError: await message.answer("❌ Неверные параметры")
        return

    if not is_subscribed:
        info_cmds = ["/top", "/help", "/start", "/mysub", "/admin"]
        if not any(cmd in message.text for cmd in info_cmds):
            not_sub = await check_required_subs(user_id)
            if not_sub:
                await message.answer(
                    "🔔 <b>Подпишитесь на каналы:</b>\n\n" + "\n".join(f"• {ch}" for ch in not_sub) +
                    "\n\nПосле подписки нажмите <b>✅ Проверить</b>",
                    reply_markup=kb_check_channels(not_sub), parse_mode="HTML"); return

    PROCESSING_CMDS = ['/hud', '/hp', '/blood', '/tree', '/vctree', '/kp', '/carmenu',
                       '/speedometer', '/road', '/casino', '/pickup', '/timecyc', '/colorcyc',
                       '/particle', '/genrl', '/merger', '/aitimecyc', '/weapon']
    is_processing_cmd = any(cmd in message.text for cmd in PROCESSING_CMDS)
    if is_processing_cmd:
        if not is_subscribed:
            queue_msg = await message.answer("⏳ <b>Ваш запрос в очереди...</b>", parse_mode="HTML")
            await queue_acquire(False)
            try: await queue_msg.delete()
            except: pass
        else:
            await queue_acquire(True)
        asyncio.create_task(auto_cleanup())

    try:
        if '/hud1' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /hud1 #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud1.zip", "hud1", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Hud готов!</b>', parse_mode="HTML", force_document=True)
            await asyncio.to_thread(shutil.rmtree, work_dir)

        if '/hud2' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /hud2 #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud2.zip", "hud2", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Hud готов!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/hud3' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /hud3 #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud3.zip", "hud3", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Hud готов!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/hud4' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /hud4 #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud4.zip", "hud4", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Hud готов!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/hp1' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /hp1 #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp1.zip", "hp1", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Элементы худа готовы!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/hp2' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /hp2 #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp2.zip", "hp2", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Элементы худа готовы!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/hp3' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /hp3 #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp3.zip", "hp3", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Элементы худа готовы!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/blood' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /blood #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/blood.zip", "blood", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваша кровь готова!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/tree' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /tree #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/tree.zip", "tree", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваши деревья готовы!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/vctree' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /vctree #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/vctree.zip", "vctree", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваши деревья готовы!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        for kp_num in range(1, 10):
            cmd = f'/kp{kp_num}'
            if cmd in j:
                y = await message.answer("Обрабатываю...")
                try: hex_color = j[1]
                except: await message.answer(f"❔ Пример: {cmd} #FF0000 0.4"); return
                try: alpha = float(j[2])
                except: alpha = 1.0
                work_dir, output_zip_path = await color_optimized(hex_color, f"zip/kp{kp_num}.zip", f"kp{kp_num}", alpha)
                await y.delete()
                await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode="HTML", force_document=True)
                shutil.rmtree(work_dir)

        if '/carmenu' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /carmenu #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/carmenu.zip", "carmenu", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваше меню машины готово!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/speedometer' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /speedometer #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/speedometer.zip", "speedometer", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваш спидометр готов!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/road' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /road #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/road.zip", "road", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Вари дороги готовы!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/casino' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /casino #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/casino.zip", "casino", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваш худ казино готов!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if '/pickup' in j:
            y = await message.answer("Обрабатываю...")
            try: hex_color = j[1]
            except: await message.answer("❔ Пример: /pickup #FF0000 0.4"); return
            try: alpha = float(j[2])
            except: alpha = 1.0
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/pickup.zip", "pickup", alpha)
            await y.delete()
            await t_client.send_file(message.chat.id, output_zip_path, caption='<b>⚡️Ваши пикапы готовы!</b>', parse_mode="HTML", force_document=True)
            shutil.rmtree(work_dir)

        if "/edit" in message.text:
            b2 = InlineKeyboardBuilder()
            b2.row(types.InlineKeyboardButton(text="Открыть Photoshop", web_app=types.WebAppInfo(url="https://pixlr.com/ru/express/")))
            await message.answer("<b>⚡️Держи редактор:</b>", reply_markup=b2.as_markup(), parse_mode='HTML')

        if "/timecyc" in message.text and len(j) >= 5:
            y = await message.answer("Обрабатываю...")
            output_file_path = await timecyc(j)
            await y.delete()
            await t_client.send_file(message.chat.id, output_file_path, caption='<b>⚡️TimeCycle готов!</b>', parse_mode="HTML", force_document=True)
            if os.path.exists(output_file_path): os.remove(output_file_path)
        elif "/timecyc" in message.text and len(j) < 5:
            await message.answer("❔ Пример: /timecyc #НизНеба #ВерхНеба #Облака #Солнце")

        elif "/colorcyc" in message.text and len(j) >= 2:
            y = await message.answer("Обрабатываю...")
            if is_float(j[1]):
                black = j[1]
                grn1 = await colorcyc(black, black, black)
            else:
                hex_color = j[1]
                r1, g1, b1 = ImageColor.getrgb(hex_color)
                r_str, g_str, b_str = (str(round(c / 100, 3)) for c in [r1, g1, b1])
                grn1 = await colorcyc(r_str, g_str, b_str)
            await y.delete()
            await t_client.send_file(user_id, grn1, caption='⚡️<b>Ваш colorcycle готов!</b>', parse_mode='HTML')
            os.remove(grn1)
        elif "/colorcyc" in message.text:
            await message.answer("❔ Пример: /colorcyc 1.2 или /colorcyc #FF0000")

        elif "/checkcolor" in message.text and len(j) >= 2:
            y = await message.answer("Обрабатываю...")
            hex_color = j[1]
            image_path = await kvadratik(hex_color)
            await y.delete()
            await t_client.send_file(user_id, image_path, caption=f'🎨<b>Палитра цвета - {hex_color}</b>', parse_mode="HTML")
            os.remove(image_path)
        elif "/checkcolor" in message.text:
            await message.answer("❔ Пример: /checkcolor #FF0000")

        elif '/wpr' in j:
            try: preset_arg = j[1]
            except: await message.answer("❔ Пример: /wpr 2"); return
            if preset_arg not in PRESETS:
                await message.answer("❔ Доступные пресеты: 1, 2, 3, 4"); return
            weapon_user_settings[user_id] = preset_arg
            preset = PRESETS[preset_arg]
            await message.answer(f"✅ <b>Пресет weapon сохранён</b>\n🗂 {preset['name']}\n📄 {preset['desc']}\n\nОтправь <b>/weapon &lt;PT&gt; &lt;RAZB&gt;</b>", parse_mode="HTML")

        elif '/weapon' in j and len(j) >= 3:
            try: PT = int(j[1]); RAZB = int(j[2])
            except: await message.answer("❌ PT и RAZB должны быть числами.\nПример: /weapon 9 50"); return
            preset_id = weapon_user_settings.get(user_id, "1")
            preset = PRESETS[preset_id]
            y = await message.answer("⏳ Обрабатываю...")
            n = generate_random_string(8)
            tmp_folder = f"work/work_weapon/{n}"
            zip_path = f"work/work_weapon/{n}.zip"
            try:
                os.makedirs("work/work_weapon", exist_ok=True)
                shutil.copytree(preset["folder"], tmp_folder)
                apply_weapon_params(tmp_folder, PT, RAZB)
                build_weapon_zip(tmp_folder, zip_path)
                await y.delete()
                await bot.send_document(message.chat.id, FSInputFile(zip_path),
                    caption=(f"🔫 <b>Weapon готов!</b>\n\n📦 Патроны: <b>{PT}</b>\n🎯 Разброс: <b>{RAZB}</b>\n🗂 Пресет: {preset['name']}\n📄 {preset['desc']}"), parse_mode="HTML")
            except Exception as e: await y.edit_text(f"❌ Ошибка: {e}")
            finally:
                shutil.rmtree(tmp_folder, ignore_errors=True)
                if os.path.exists(zip_path): os.remove(zip_path)

        elif '/particle' in message.text and len(j) >= 2:
            try:
                y = await message.answer("Обрабатываю...")
                if len(j) < 3:
                    await bot.send_message(user_id, "Неверный формат. Используйте: /particle <цвет> <размер>"); return
                rgb = ImageColor.getrgb(j[1])
                r_val, g_val, b_val = map(str, rgb)
                q = generate_random_string(6)
                work_dir_p = Path(f'work/work_BLOOD/{q}')
                work_dir_p.mkdir(parents=True, exist_ok=True)
                grn1_path = work_dir_p / f'{q}_particle.cfg'
                with open('particleCH.cfg', 'r') as infile: t = infile.read()
                t = t.replace("r22", r_val).replace("g22", g_val).replace("b22", b_val)
                if len(j) > 2:
                    t = t.replace("Q11", j[2]).replace("U11", j[4] if len(j) > 4 else "0").replace("R11", j[5] if len(j) > 5 else "0").replace("T11", j[3] if len(j) > 3 else "0")
                with open(grn1_path, 'w') as outfile: outfile.write(t)
                await y.delete()
                await t_client.send_file(user_id, grn1_path, caption='⚡️ Ваш particle.cfg готов!')
            except Exception as e: await bot.send_message(user_id, f"Ошибка: {e}")
            finally:
                if 'work_dir_p' in locals() and work_dir_p.exists(): shutil.rmtree(work_dir_p)

        elif '/btx' in j:
            parts = message.text.strip().split()
            block_arg = parts[1].lower() if len(parts) > 1 else None
            quality_arg = parts[2].lower() if len(parts) > 2 else None
            errors = []
            bw2, bh2 = BTX_DEFAULT_BLOCK
            quality2 = BTX_DEFAULT_QUALITY
            quality_name2 = "medium"
            if block_arg:
                if block_arg in BTX_BLOCK_MAP: bw2, bh2 = BTX_BLOCK_MAP[block_arg]
                else: errors.append(f"❌ Неверный блок: <code>{block_arg}</code>. Доступные: {', '.join(BTX_BLOCK_MAP.keys())}")
            if quality_arg:
                if quality_arg in BTX_QUALITY_MAP: quality2 = BTX_QUALITY_MAP[quality_arg]; quality_name2 = quality_arg
                else: errors.append(f"❌ Неверное качество: <code>{quality_arg}</code>. Доступные: {', '.join(BTX_QUALITY_MAP.keys())}")
            if errors: await message.answer("\n".join(errors), parse_mode="HTML"); return
            btx_user_settings[user_id] = {"block": (bw2, bh2), "quality": quality2, "quality_name": quality_name2}
            await message.answer(f"✅ <b>Настройки BTX сохранены</b>\n🔷 Блок: <code>{bw2}x{bh2}</code>\n⚙️ Качество: <code>{quality_name2}</code>", parse_mode="HTML")

        elif '/search' in j:
            try: args = j[1]
            except: await message.answer("❔ Пример: /search 11"); return
            query = j[1].strip()
            results = search_in_skins(query)
            if results is None: await message.answer("Ошибка при чтении файла skins.txt")
            elif not results: await message.answer(f"Нет информации о - {query}")
            else:
                id_xyina, name_xyina = results[0]
                attached_files = await filerpoisk(id_xyina, name_xyina, message)
                response = []
                if attached_files: response.extend(attached_files); response.append("")
                response.append(f"ID - {id_xyina}"); response.append(f"NAME - {name_xyina}")
                if not attached_files: await message.answer("\n".join(response))

        elif '/skin' in j:
            try:
                await t_client.send_file(user_id, f"skin/{j[1]}.dff", caption='⚡️<b>Держите скин!</b>', parse_mode="HTML", force_document=True)
                await t_client.send_file(user_id, f"texture/texture_{j[1]}.zip", caption='⚡️<b>Держите текстуры!</b>', parse_mode="HTML", force_document=True)
            except: await message.answer("Такого названия нет")

        elif '/car' in j:
            try: await t_client.send_file(user_id, f"car/{j[1]}.mod", caption='⚡️<b>Держите машину!</b>', parse_mode="HTML", force_document=True)
            except: await message.answer("Такого названия нет")

        elif "/merger" in message.text:
            if len(j) < 3:
                await message.answer("Неверный формат. Используйте: /merger <что копировать> <название>\nВарианты: tree, logo, bild"); return
            r2 = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            y = await message.answer("⏳<b>Обрабатываю...</b>", parse_mode="HTML")
            clas = j[1].lower()
            name = j[2]
            if clas == "tree": suffix = Tree
            elif clas == "logo": suffix = FILE_SUFFIXES
            elif clas == "bild": suffix = bild
            else: await message.answer("Неизвестный класс. Варианты: tree, logo, bild"); return
            data = {name: suffix}
            with open(f'Merger_{r2}.json', 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)
            await y.delete()
            await t_client.send_file(user_id, f'Merger_{r2}.json', caption=f'⚡<b>Ваш Merger.json</b>', parse_mode="HTML")
            os.remove(f'Merger_{r2}.json')

        elif "/aitimecyc" in message.text:
            if len(j) < 2:
                await message.answer("❔ Формат: /aitimecyc <описание>\nПример: /aitimecyc закат с алыми облаками"); return
            description = message.text.replace("/aitimecyc", "", 1).strip()
            y = await message.answer("🤖 <b>Генерирую таймсус...</b>", parse_mode="HTML")
            try:
                loop = asyncio.get_running_loop()
                ai_colors = await loop.run_in_executor(None, _sync_aitimecyc, description)
                json_path = await asyncio.to_thread(generate_aitimecyc_json, ai_colors)
                preview_path = await asyncio.to_thread(generate_sky_preview, ai_colors, description)
                sky_top_hex = '#{:02X}{:02X}{:02X}'.format(*ai_colors["SkyTopRGB"])
                sky_bot_hex = '#{:02X}{:02X}{:02X}'.format(*ai_colors["SkyBottomRGB"])
                cloud_hex = '#{:02X}{:02X}{:02X}'.format(*ai_colors["CloudRGB"])
                sun_hex = '#{:02X}{:02X}{:02X}'.format(*ai_colors["SunCoreRGB"])
                await y.delete()
                await t_client.send_file(user_id, preview_path,
                    caption=(f"🎨 <b>AI TimeCyc:</b>\n<i>{description}</i>\n\n"
                             f"🌅 SkyTop: <code>{sky_top_hex}</code>\n🌄 SkyBottom: <code>{sky_bot_hex}</code>\n"
                             f"☁️ Cloud: <code>{cloud_hex}</code>\n☀️ Sun: <code>{sun_hex}</code>"), parse_mode="HTML")
                await t_client.send_file(user_id, json_path, caption='<b>⚡️ timecyc.json готов!</b>', parse_mode="HTML", force_document=True)
                os.remove(json_path); os.remove(preview_path)
            except Exception as e: await message.answer(f"❌ Ошибка: {e}")

        elif "/aicolor" in message.text:
            if len(j) < 2:
                await message.answer("❔ Пример: /aicolor свет от луны"); return
            description = message.text.replace("/aicolor ", "").strip()
            hex_color = get_hex_from_description(description)
            image_path = await kvadratik(hex_color)
            await t_client.send_file(user_id, image_path, caption=f'🎨<b>Hex цвет - {hex_color}</b>', parse_mode="HTML")
            os.remove(image_path)

        elif "/randcolor" in message.text:
            hex_color = random_color()
            image_path = await kvadratik(hex_color)
            await t_client.send_file(user_id, image_path, caption=f'🎨<b>Hex цвет - {hex_color}</b>', parse_mode="HTML")
            os.remove(image_path)

        elif "/promo" in message.text:
            parts_p = message.text.split()
            if len(parts_p) < 2:
                await message.answer(
                    "🎟 <b>Активация промокода</b>\n\nФормат: <code>/promo КОД</code>",
                    parse_mode="HTML")
            else:
                code_p = parts_p[1].upper()
                ok_p, promo_p, err_p = use_promo(code_p, user_id)
                if not ok_p:
                    await message.answer(err_p, parse_mode="HTML")
                else:
                    b_p = InlineKeyboardBuilder()
                    for pl in SUBSCRIPTION_PLANS:
                        np = apply_promo_to_plan(pl, promo_p)
                        b_p.button(text=np["emoji"] + " " + np["label"] + " — " + str(np["stars"]) + "⭐",
                                   callback_data="promo_apply_" + str(pl["stars"]) + "_" + code_p)
                    b_p.adjust(1)
                    info_lines = ["✅ <b>Промокод " + code_p + " активирован!</b>"]
                    if promo_p["name"]:    info_lines.append("📝 " + promo_p["name"])
                    if promo_p["comment"]: info_lines.append("💬 " + promo_p["comment"])
                    if promo_p["link"]:    info_lines.append("🔗 " + promo_p["link"])
                    if promo_p["custom_stars"]:
                        info_lines.append("💰 Спеццена: " + str(promo_p["custom_stars"]) + "⭐")
                    elif promo_p["discount_pct"]:
                        info_lines.append("💸 Скидка: -" + str(promo_p["discount_pct"]) + "%")
                    info_lines.append("\nВыберите тариф:")
                    await message.answer("\n".join(info_lines), reply_markup=b_p.as_markup(),
                                         parse_mode="HTML")

        elif "/refbal" in message.text:
            _, _, bal = get_ref_stats(user_id)
            await message.answer(
                "💰 <b>Реферальный баланс: " + str(bal) + " ⭐</b>\n\n"
                "Для вывода напишите @" + SUPPORT_USERNAME, parse_mode="HTML")

        elif "/batch" in message.text:
            parts_b = message.text.split(None, 2)
            if len(parts_b) < 2:
                await message.answer(
                    "📦 <b>Пакетная обработка</b>\n\n"
                    "Формат: <code>/batch &lt;команда&gt; [подпись]</code>\n"
                    "Затем отправляй файлы по одному.\n"
                    "Для обработки — <code>/stopbatch</code>\n\n"
                    "Пример: <code>/batch /color #FF0000</code>",
                    parse_mode="HTML"); return
            batch_cmd = parts_b[1]
            batch_cap = parts_b[2] if len(parts_b) > 2 else batch_cmd
            start_batch(user_id, batch_cmd, batch_cap)
            await state.set_state(BatchFSM.collecting)
            await message.answer(
                "✅ <b>Пакетный режим запущен!</b>\n\n"
                "Команда: <code>" + batch_cmd + "</code>\n"
                "Отправляй файлы. Когда закончишь — <code>/stopbatch</code>",
                parse_mode="HTML")

        elif "/stopbatch" in message.text:
            batch = get_batch(user_id)
            if not batch:
                await message.answer("❌ Нет активной пакетной сессии."); return
            files_list = batch.get("files", [])
            clear_batch(user_id)
            await state.clear()
            if not files_list:
                await message.answer("❌ Файлы не получены, сессия отменена."); return
            await message.answer(
                f"⏳ <b>Обрабатываю {len(files_list)} файл(ов)…</b>\n"
                "Результаты придут по мере готовности.", parse_mode="HTML")

        elif "/ref" in message.text:
            ref_link_u = get_ref_link(user_id)
            tot_r, paid_r, bal_r = get_ref_stats(user_id)
            next_tier = next(((t, d) for t, d in sorted(
                [(1,10),(10,15),(20,20),(50,25)], key=lambda x: x[0]
            ) if t > paid_r), None)
            tier_txt = ("\n📈 До след. уровня: ещё " + str(next_tier[0]-paid_r) +
                        " рефералов (" + str(next_tier[1]) + "%)") if next_tier else "\n🏆 Максимум!"
            await message.answer(
                "👥 <b>Реферальная программа</b>\n\n"
                "🔗 Ваша ссылка:\n<code>" + ref_link_u + "</code>\n\n"
                "📊 Статистика:\n"
                "  Приглашено: <b>" + str(tot_r) + "</b>\n"
                "  Оплатили: <b>" + str(paid_r) + "</b>\n"
                "  Баланс: <b>" + str(bal_r) + "⭐</b>" +
                tier_txt + "\n\n"
                "💎 <b>Скидки для приглашённых:</b>\n"
                "  1+ → -10% | 10+ → -15% | 20+ → -20% | 50+ → -25%\n\n"
                "Вы получаете <b>15%</b> от покупки реферала ⭐",
                parse_mode="HTML")

        elif "/support" in message.text:
            is_prem = is_subscribed
            b_sup = InlineKeyboardBuilder()
            b_sup.button(text="📝 Создать обращение", callback_data="support_new")
            await message.answer(
                "🎫 <b>Техническая поддержка " + BOT_NAME + "</b>\n\n"
                + ("💎 Premium-пользователи обслуживаются приоритетно.\n\n" if is_prem else "")
                + "Нажмите кнопку ниже чтобы создать обращение.\n"
                "Или напишите напрямую: @" + SUPPORT_USERNAME,
                reply_markup=b_sup.as_markup(), parse_mode="HTML")

        elif "/review" in message.text:
            parts_rv = message.text.split(None, 2)
            if len(parts_rv) < 2:
                await message.answer(
                    "⭐ <b>Оставить отзыв</b>\n\nФормат: <code>/review 5 Отличный бот!</code>\nОценка от 1 до 5",
                    parse_mode="HTML"); return
            try:
                rating_rv = int(parts_rv[1])
                if not 1 <= rating_rv <= 5:
                    raise ValueError
            except:
                await message.answer("❌ Оценка должна быть от 1 до 5"); return
            text_rv = parts_rv[2] if len(parts_rv) > 2 else ""
            add_review(user_id, rating_rv, text_rv)
            stars_rv = "⭐" * rating_rv
            await message.answer("✅ <b>Спасибо за отзыв!</b> " + stars_rv, parse_mode="HTML")

        elif "/help" in message.text:
            await message.answer("""<b>Привет👋 Вот возможности бота:</b>

<b>📌 Основные команды:</b>
/start — начать работу с ботом
/mysub — информация о подписке
/top — топ активных пользователей
/edit — запуск фотошопа
/help — помощь

<b>🎨 Работа с цветом:</b>
/color - покраска изображений
/recolor - перекраска цвета
/checkcolor - палитра цвета
/aicolor - цвет по описанию
/randcolor - случайный приятный цвет
/overlay - наложение изображения
/filters - фильтры
/hud1-4 - перекраска hud
/hp1-3 - перекраска элементов hud
/blood - кровь | /tree - листва | /vctree - VC листва
/kp1-9 - кнопки | /carmenu - меню машины
/speedometer - спидометр | /road - дороги
/casino - казино | /pickup - пикапы

<b>📂 Создание файлов:</b>
/weapon - weapon.dat | /timecyc - TimeCycle
/colorcyc - ColorCycle | /particle - кровь
/genrl - звуки бр | /bpc - шифровка bpc
/nri - сборки nonerai | /merger - Merger
/index - индексация | /aitimecyc - AI TimeCycle

<b>✂️ Нарезка:</b>
/hudcut - нарезка hud | /map - нарезка map
/remap - восстановить map | /rehud - восстановить hud

<b>🌐 Дополнительно:</b>
/ptk - пипетка | /aim - прицел
/weather - погода | /compress - сжатие
/search - поиск скина | /btx - настройка BTX | /wpr - веапон

<b>📁 Автоматически:</b>
<i>.btx/.png/.jpg/.zip</i> — обработка BTX/PNG/JPG
<i>.txd</i> — расшифровка TXD
<i>.bpc</i> — расшифровка bpc
<i>.ifp</i> — расшифровка анимаций
<i>.cls</i> — расшифровка коллизий
<i>.mod</i> — расшифровка моделей
<i>timecyc.dat</i> — конвертация в Black Russia
<i>timecyc.json</i> — цвета из Timecyc""", parse_mode='HTML')

        elif "/sub" in message.text and len(j) >= 3:
            admin_status_row = execute_sql_query("SELECT admin FROM users WHERE chat_id=?", (user_id,), fetchone=True)
            if admin_status_row and admin_status_row[0] == 'True':
                target_user_id = int(j[1])
                target_user_row = execute_sql_query("SELECT username FROM users WHERE chat_id=?", (target_user_id,), fetchone=True)
                if target_user_row:
                    target_username = target_user_row[0]
                    action = j[2]
                    if len(j) == 4 and action == 'True':
                        expiry_date_str = j[3]
                        try:
                            datetime.datetime.strptime(expiry_date_str, "%d.%m.%Y")
                            execute_sql_query("UPDATE users SET sub='True', time=? WHERE chat_id=?", (expiry_date_str, target_user_id))
                            await message.answer(f'Пользователю {target_username} выдана подписка до {expiry_date_str}!')
                        except ValueError: await message.answer("Неверный формат даты! Используйте %d.%m.%Y.")
                    elif action == 'False':
                        execute_sql_query("UPDATE users SET sub='False', time=NULL WHERE chat_id=?", (target_user_id,))
                        await message.answer(f"У пользователя {target_username} забрана подписка!")
                    else: await message.answer("Неверный формат команды!")
                else: await message.answer(f"Пользователь с ID {target_user_id} не найден.")
            else: await message.answer("У вас нет прав администратора.")

        elif "/kotek" in message.text:
            admin_status_row = execute_sql_query("SELECT admin FROM users WHERE chat_id=?", (user_id,), fetchone=True)
            if admin_status_row and admin_status_row[0] == 'True':
                all_users = execute_sql_query("SELECT chat_id FROM users", fetchall=True)
                message_to_send2 = message.text.replace("/kotek", "").strip()
                if message_to_send2:
                    for user_row in all_users:
                        uid2 = user_row[0]
                        try: await bot.send_message(uid2, message_to_send2); await asyncio.sleep(0.1)
                        except Exception as e: print(f"Не удалось отправить {uid2}: {e}")
                    await message.answer("Рассылка завершена.")
                else: await message.answer("Введите текст рассылки после команды.")
            else: await message.answer("У вас нет прав администратора.")

        elif "/send" in message.text:
            admin_status_row = execute_sql_query("SELECT admin FROM users WHERE chat_id=?", (user_id,), fetchone=True)
            if admin_status_row and admin_status_row[0] == 'True':
                try:
                    target_id_str = j[1]
                    target_id = int(target_id_str)
                    text_to_send = message.text.replace("/send", "").replace(target_id_str, "").strip()
                    if text_to_send:
                        await bot.send_message(target_id, text_to_send)
                        await message.answer(f"Сообщение отправлено пользователю {target_id}.")
                    else: await message.answer("Введите текст сообщения после ID получателя.")
                except ValueError: await message.answer("Неверный формат ID.")
                except Exception as e: await message.answer(f"Ошибка: {e}")
            else: await message.answer("У вас нет прав администратора.")

    finally:
        if is_processing_cmd:
            await queue_release(is_subscribed)

async def main():
    await setup_work_dirs()
    init_semaphores()
    await p_app.start()
    await t_client.start(bot_token=BOT_TOKEN)
    try:
        await dp.start_polling(bot)
    finally:
        await p_app.stop()
        await t_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
