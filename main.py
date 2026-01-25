from aiogram import Bot, Dispatcher, F, types
import asyncio
import logging
import sqlite3
import os
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
import string
import random
from PIL import ImageColor, Image, ImageDraw, ImageFont
from aiogram.types import FSInputFile, BufferedInputFile
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

TOKEN = '7062207808:AAF5vGV9ndvzvW2Ray0rxTM9RsGWMuB5gBw'
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
loging_id = [2080411409]
bot = Bot(token=TOKEN)
boti = Bot(token="7079077190:AAFosQVHAePab0Ck4lkVue8vY0AqnISPmEI")
NOT_HI_MESSAGE = "Здравствуйте! Чтобы использовать бота, вам необходимо оформить подписку @keedboy016"
length = 4
DB_PATH = 'users.db'
FILE_SUFFIXES = ['logobrkrasnodar', 'logobrkaliningrad', 'logobrbelgorod', 'logobrizhevsk', 'logobrgray', 'logobryakutsk', 'logobrvoronezh', 'logobrcherry', 'logobrcrimson', 'logobrkrasnoyarsk', 'logobrnorilsk', 'logobrorel', 'logobrbratsk', 'logobrlipetsk', 'logobrtolyatti', 'logobrcherepovets', 'logobrkirov', 'logobrkostroma', 'logobrspb', 'logobrastrakhan', 'logobrarkhangelsk', 'logobrstavropol', 'logobrvladivostok', 'logobrmagenta', 'logobrbarnaul', 'logobrmoscow', 'logobrvladimir', 'logobrrostov', 'logobraqua', 'logobrsochi', 'logobrarzamas', 'logobryellow', 'logobrnovgorod', 'logobrchelyabinsk', 'logobrorange', 'logobrkazan', 'logobrpodolsk', 'logobrkhabarovsk', 'logobrsaratov', 'logobrtver', 'logobranapa', 'logobrvologda', 'logobrkemerovo', 'logobrchita', 'logobrgreen', 'logobryaroslavl', 'logobrchoco', 'logobrmakhachkala', 'logobrpskov', 'logobrgrozny', 'logobrtambov', 'logobrekb', 'logobrcheboksary', 'logobrvladikavkaz', 'logo', 'logobrmagadan', 'logobrred', 'logobrplatinum', 'logobrsmolensk', 'logobrwhite', 'logobrvolgograd', 'logobrpurple', 'logobrnovosib', 'logobrtula', 'logobrtaganrog', 'logobrmurmansk', 'logobrsurgut', 'logobrufa', 'logobrblack', 'logobrchilli', 'logobrlime', 'logobrperm', 'logobromsk', 'logobrazure', 'logobrice', 'logobrbryansk', 'logobrkursk', 'logobrryazan', 'logobrpenza', 'logobrirkutsk', 'logobrblue', 'logobrsamara', 'logobrindigo', 'logobrkaluga', 'logobrtyumen', 'logobrorenburg', 'logobrgold', 'logobrulyanovsk', 'logobrpink', 'logobrtomsk', 'logobrivanovo']
MAX_FILE_SIZE = 1024 * 1024 * 50
Tree = ['417f945c', '43tree1', '43tree2', '43tree3', '43tree4', '43tree5', '43tree6', '43tree7', '43tree8', '43tree9', '44tree1', '44tree2', '44tree4', '44tree5', '9event_treesbg1', '9event_treesbg2', 'apat_flowers', 'AppleTree', 'AucTreeCrone8712', 'AucWeed8163', 'Bdup2_plant', 'beregd1_elka', 'beregd1_listv2', 'BRG_flowers1', 'BRTREE_Atl_B', 'BRTREE_leaf1', 'BRTREE_leaf1o', 'BRTREE_leaf2', 'BRTREE_leaf2o', 'BRTREE_leaf3', 'BRTREE_leaf4', 'BRTREE_leaf4o', 'BRTREE_leaf5', 'BRTREE_leaf5o', 'BRTREE_leaf6', 'BRTREE_leaf7', 'BRTREE_leaf8', 'BRTREE_leaf8o', 'BukTree1', 'BukTree2', 'bysaevo_grasssandmix', 'byssch_flower1', 'byssch_flower2', 'byssch_flower3', 'byssch_flower4', 'byssch_flower5', 'bys_appletree', 'bys_cherrytree', 'bys_flowers', 'bys_plumtree', 'bys_wires', 'b_craet1_4_ca', 'cactusL', 'CasinoNor3864', 'cj_flower(hi_res)cj_flower_a(h', 'CJ_FLOWER_256cj_flower_a', 'cj_leaf_cheesecj_leaf_cheese_a', 'CJ_PLANT', 'cottagetuya-2', 'cottagetuya', 'derevachkacrb', 'derevo', 'derevo3', 'derevoclub8201', 'derevoclub8201st', 'derevoclub82021', 'derevoclub82022', 'derevoclub8202st', 'derevoclub8203', 'derevoclub8203st', 'derevopar7901', 'derevopar7902', 'derevopar7903', 'derevopar7904', 'derevopar7905', 'derevo_krov', 'edovo_coundom_flower', 'f', 'fialkiflowers', 'flowert', 'free grass', 'freegrass', 'gameleaf01_64', 'gameleaf02_64', 'grass1', 'GrassAlpha7453', 'GrassA_02', 'GrassA_04', 'GrassA_05', 'GrassA_15', 'GrassA_15_1', 'GrassA_16', 'GrassA_20', 'GrassVazMast', 'Grass_00', 'grass_gen256old', 'grass_green_long', 'grass_green_med', 'gz_e2_fishleaf01gz_e2_fishleaf', 'gz_e2_fishleaf02gz_e2_fishleaf', 'gz_e2_fishleaf03gz_e2_fishleaf', 'gz_e2_leaf_cheesegz_e2_leaf_ch', 'hot_flowers1', 'int_fsb_flow1', 'int_fsb_flow1a', 'int_pr_flow1', 'int_pr_flow2', 'izbamishura', 'kbplanter_plants1', 'kb_balcony_ferns', 'kb_balcony_ferns_genintgeneric', 'kb_ivy2_256', 'klubnika', 'km_flowerpic2', 'km_plant1', 'kolosya_rog', 'KOR_grape', 'krapiva_list', 'kustik1', 'kustik2', 'KustRog8716', 'kust_farm1', 'kyst3', 'l', 'lager_trees1', 'lager_trees2', 'lag_reeds1', 'LeavesTropical0141_1', 'LeavesTropical0202_1', 'LeavesTropical0218_1', 'lentisk', 'lf_arzflowers1', 'list4', 'LODBRTREE_1_6_7_8', 'LODBRTREE_2_3', 'LODBRTREE_4_5_9_10', 'LODBRTREE_atl', 'LODbuktree2_a889', 'LODbuktree3_a889', 'LODbuktree4_a889', 'LODbuktree5_a889', 'LODbuktree6_a889', 'LODbuktree7_a889', 'LODbuktree8_a889', 'LODH_leaftree_big', 'LODH_leaftree_med', 'LODH_leaftree_root', 'LODH_leaftree_sml', 'LODH_leaftree_vol', 'LODH_pinetree1', 'LODH_pinetree2', 'LODH_pinetree3', 'LODH_Rdeadtree', 'lopux_koluchka', 'lopux_list', 'moss_shrek_a889', 'mp_flowerbush', 'mp_gs_flowerwall', 'mp_h_acc_vase_flowers_04', 'mp_h_acc_vase_leaves_03mp_h_acc', 'newtreeleaves128', 'newtreeleavesb128', 'NGMishura6121', 'NGMishura6121_2', 'nonalpha_compressedLOD_treeRUBH', 'NRock_kust1', 'NRock_kust2', 'Palm0471', 'palm8204', 'PalmArecaceae144', 'PalmWall2947', 'planta252', 'planta256', 'plantc256', 'PlantH1741', 'potato', 'rn_hell_flow', 'rus_bigORGANGEflower', 'rus_grasstype2', 'rus_grassTYPE3', 'rus_grasstype4_flowers', 'rus_whiteflower_ingrass', 'R_Berez1_b', 'R_Berez1_t', 'R_Dub1', 'R_hln_MgkLeaf1', 'R_hln_MgkLeaf2', 'R_hln_MgkLeaf3', 'R_Listv1', 'salad', 'sm_Agave_1', 'sm_Agave_2', 'sm_minipalm1', 'sm_potplant1', 'starflower2', 'starflower2wht', 'starflower3', 'starflower3prpl', 'starflower3yel', 'Strip_plant', 'stvolListv1', 'svekla', 'tikva', 'tomato', 'TomatoFarm', 'Tree', 'tree19Mi', 'treeCRB221_1', 'TreeCron9716', 'TreeCron9716_2', 'trees_vetkagreen5', 'treewillow99', 'tree_lodderevo1', 'tree_lodeubeech1', 'tree_lodfikovnik', 'tree_lodkastan', 'tree_lodlinden', 'tree_lodpaper_der1', 'tree_lodpaper_der2', 'tree_lodwillow', 'TREE_STUB1', 'tuyaclub8205', 'T_br5_FlwrVs', 'T_CM_Leaf_D', 'T_flg_Cl_Ch_A', 'T_flg_Cl_Ch_B', 'T_flg_Cl_CrTr_A', 'T_flg_Cl_CrTr_B', 'T_flg_Cl_Dead_A', 'T_flg_Cl_Hdg_A', 'T_flg_Cl_Lndn_A', 'T_flg_Cl_Mpl_A', 'T_flg_Cl_Poplar_A', 'T_flg_Cl_Shbrr_A', 'T_flg_Cl_Shbrr_B', 'T_flg_Cl_Th_A', 'T_flg_Cl_Th_B', 'T_flg_Cl_Th_C', 'T_flg_DeadBrunch_A', 'T_flg_DeadBrunch_B', 'T_flg_ForestGround', 'T_flg_Grss_V', 'T_flg_Grss_V2', 'T_flg_Grss_X', 'T_flg_Grss_Y', 'T_flg_Hdg_A', 'T_flg_ivy_A', 'T_flg_ivy_fall', 'T_flg_LeafA', 'T_flg_leafs', 'T_flg_Lndn_A_Low', 'T_flg_Moss_A', 'T_flg_Moss_B', 'T_flg_Moss_C', 'T_flg_NeedleA', 'T_flg_PalmLeaf_A', 'T_flg_ShoreGrassA', 'T_nn_TreesLODtex_a', 'T_nn_TreesLODtex_b', 'T_nn_TreesLODtex_c', 'UGPRST_der1', 'vk_int_gaz_grass1', 'vk_m9_ev_kust', 'WH_flowers1', 'yellosmallflowers', 'z-H-dc-Fern1', 'z_H_atl_grss_014']
bild = ['reclam65', 'reclam66', 'Billb_SanVice', 'BLBRD_3_889', 'reclam67', 'BLBRD_1_a889', 'Billb_MyriadIslands', 'reclam64', 'Billb_AlienCity', 'bilb_sign1', 'BLBRD_btn1_a889', 'BLBRD_5_889', 'reclam69', 'BLBRD_main1_a889', 'Billb_GTABer', 'reclam68', 'BLBRD_6_889', 'reclam62', 'Billb_GostownParadise', 'reclam63', 'Billb_YouAreHere', 'bilb_sign2', 'Billb_GTAUnited', 'BLBRD_4_889', 'BLBRD_2_889']
pvrtex_tool = "PVRTexToolCLI"

def compute_data_offset(zip_path: Path, header_offset: int) -> int:
    with zip_path.open('rb') as f:
        f.seek(header_offset)
        header = f.read(30)
        if len(header) < 30:
            raise IOError(f"Unexpected short local header at offset {header_offset}")
        file_name_len = int.from_bytes(header[26:28], 'little')
        extra_field_len = int.from_bytes(header[28:30], 'little')
        data_offset = header_offset + 30 + file_name_len + extra_field_len
        return data_offset

def generate_bpcmeta(zip_path_str: str, output_path_str: str = None):
    zip_path = Path(zip_path_str)
    if output_path_str:
        out_path = Path(output_path_str)
    else:
        out_path = zip_path.with_suffix('.bpcmeta')

    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")

    entries = []
    with zipfile.ZipFile(zip_path, 'r') as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            lower = info.filename.lower()
            if not lower.endswith(('.mp3', '.wav', '.ogg')):
                continue
            header_offset = getattr(info, 'header_offset', None)
            if header_offset is None:
                raise RuntimeError(f"No header_offset for {info.filename}; Python's zipfile lacks it.")
            data_offset = compute_data_offset(zip_path, header_offset)
            comp_size = int(info.compress_size)

            is_mp3_flag = 1 if lower.endswith('.mp3') else 0

            entries.append({
                'name': info.filename,
                'data_offset': int(data_offset),
                'comp_size': comp_size,
                'is_mp3': is_mp3_flag
            })

    entries.sort(key=lambda e: e['name'].lower())
    out = bytearray()
    out += struct.pack('<I', len(entries))
    for e in entries:
        name_bytes = e['name'].encode('utf-8')
        if len(name_bytes) > 0xFFFF:
            raise ValueError(f"Filename too long after utf-8 encoding: {e['name']}")
        out += struct.pack('<I', e['data_offset'])
        out += struct.pack('<I', e['comp_size'])
        out += struct.pack('B', e['is_mp3'])
        out += struct.pack('<H', len(name_bytes))
        out += name_bytes

    out_path.write_bytes(out)
    print(f"bpcmeta: {out_path}  ({len(out)} bytes) -- entries: {len(entries)}")

def ror32(x: int, r: int) -> int:
    return ((x >> r) | (x << (32 - r))) & 0xFFFFFFFF

def tea_decrypt_block(data: bytearray, key: list[int], rounds: int = 8) -> None:
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
    if len(dff_data) < 12:
        return dff_data
    real_size = len(dff_data) - 12
    return dff_data[:4] + struct.pack('<I', real_size) + dff_data[8:]

def clean_dff_data(dff_data: bytearray) -> bytearray:
    end = len(dff_data)
    while end > 0 and dff_data[end - 1] == 0:
        end -= 1
    return dff_data[:end]

def decrypt_mod_to_dff(mod_bytes: bytes) -> bytes:
    magic, length, num_blocks = struct.unpack_from('<III', mod_bytes, 0)
    if magic != 0xAB921033:
        raise ValueError("invalid .mod file")
    base_key = [0x6ED9EE7A, 0x930C666B, 0x930E166B, 0x4709EE79]
    key = [ror32(k ^ 0x12913AFB, 19) for k in base_key]
    data = bytearray(mod_bytes)
    offset = 28
    for _ in range(num_blocks):
        block = data[offset:offset + 0x800]
        tea_decrypt_block(block, key)
        data[offset:offset + 0x800] = block
        offset += 0x800

    actual_length = min(length, len(mod_bytes) - 28)
    dff = bytearray(data[28:28 + actual_length])
    dff = patch_dff_header(dff)
    dff = clean_dff_data(dff)
    return bytes(dff)

async def convert_one(mod_path: str, out_dir: str, log=None):
    name = os.path.splitext(os.path.basename(mod_path))[0]
    if log:
        log(f"[~] MOD → {name}.dff")
    os.makedirs(out_dir, exist_ok=True)
    try:
        mod_bytes = open(mod_path, 'rb').read()
        dff_bytes = decrypt_mod_to_dff(mod_bytes)
        out_path = os.path.join(out_dir, name + '.dff')
        with open(out_path, 'wb') as out_f:
            out_f.write(dff_bytes)
        print(f"[✓] {name}.dff")
    except Exception as e:
        print(f"[X] error {name}: {e}")

async def batch(mod_paths: list[str], out_dir: str, log=None):
    tasks = [convert_one(p, out_dir, log) for p in mod_paths]
    await asyncio.gather(*tasks)

async def convert(mod_paths: list[str], out_dir: str, log=None):
    await batch(mod_paths, out_dir, log)

async def convert_timecyc_dat_to_json(input_path: Path, original_filename: str, temp_dir):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        entries = []
        current_entry = None

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith(';'):
                continue

            parts = re.split(r'\s+', line)
            if len(parts) < 48:
                continue

            entry = {
                "AmbientRGB": [int(parts[0]), int(parts[1]), int(parts[2])],
                "AmbientPhysicalRGB": [int(parts[3]), int(parts[4]), int(parts[5])],
                "DirectionalRGB": [int(parts[6]), int(parts[7]), int(parts[8])],
                "SkyTopRGB": [int(parts[9]), int(parts[10]), int(parts[11])],
                "SkyBottomRGB": [int(parts[12]), int(parts[13]), int(parts[14])],
                "SunCoreRGB": [int(parts[15]), int(parts[16]), int(parts[17])],
                "SunCoronaRGB": [int(parts[18]), int(parts[19]), int(parts[20])],
                "SunSize": float(parts[21]),
                "SpriteSize": float(parts[22]),
                "SpriteBrght": float(parts[23]),
                "Shad": int(parts[24]),
                "LightShad": int(parts[25]),
                "PoleShad": int(parts[26]),
                "FarClip": float(parts[27]),
                "FogStart": float(parts[28]),
                "LightGnd": float(parts[29]),
                "FluffyBottomRGB": [int(parts[30]), int(parts[31]), int(parts[32])],
                "CloudRGB": [int(parts[33]), int(parts[34]), int(parts[35])],
                "WaterRGBA": [int(parts[36]), int(parts[37]), int(parts[38]), int(parts[39])],
                "PostFX1ARGB": [int(parts[40]), int(parts[41]), int(parts[42]), int(parts[43])],
                "PostFX2ARGB": [int(parts[44]), int(parts[45]), int(parts[46]), int(parts[47])],
                "CloudAlpha": int(parts[48]) if len(parts) > 48 else 200
            }
            entries.append(entry)

        json_data = json.dumps(entries, indent=2)

        output_filename = Path(original_filename).stem + '.json'
        output_path = temp_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_data)

        return output_path
    except Exception as e:
        print(f"Error converting DAT to JSON: {e}")
        return None

async def safe_delete(file_path: Path, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            if file_path.exists():
                if file_path.is_dir():
                    shutil.rmtree(file_path, ignore_errors=True)
                else:
                    file_path.unlink(missing_ok=True)
                return True
        except Exception:
            await asyncio.sleep(0.5 * (attempt + 1))
    return False

async def convert_png_to_btx_pvr(input_path: Path, temp_ktx: Path) -> bool:
    try:
        cmd = [
            "./"+pvrtex_tool,
            "-i", str(input_path),
            "-o", str(temp_ktx),
            "-f", "ASTC_8x8,UBN,sRGB",
            "-ics", "srgb",
            "-silent"
        ]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        return temp_ktx.exists()
    except:
        return False


async def convert_btx_to_png_pvr(temp_ktx: Path, output_path: Path) -> bool:
    try:
        cmd = [
            "./"+pvrtex_tool,
            "-i", str(temp_ktx),
            "-d", str(output_path),
            "-f", "r8g8b8a8",
            "-ics", "srgb",
            "-silent"
        ]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        return output_path.exists()
    except:
        return False


async def convert_png_to_btx(input_path: Path, original_filename: str, temp_dir):
    output_filename = Path(original_filename).stem + '.btx'
    output_path = temp_dir / output_filename
    temp_ktx = temp_dir / f"temp_{random.randint(1000, 9999)}.ktx"

    f = await convert_png_to_btx_pvr(input_path, temp_ktx)
    btx_data = b'\x02\x00\x00\x00' + temp_ktx.read_bytes()
    output_path.write_bytes(btx_data)
    await safe_delete(temp_ktx)
    return output_path



async def convert_btx_to_png(input_path, original_filename: str, temp_dir):
    input_path = Path(input_path)
    output_filename = Path(original_filename).stem + '.png'
    output_path = temp_dir / output_filename
    temp_ktx = temp_dir / f"temp_{random.randint(1000, 9999)}.ktx"

    try:
        ktx_data = await asyncio.to_thread(input_path.read_bytes)
        await asyncio.to_thread(temp_ktx.write_bytes, ktx_data[4:])

        if not await convert_btx_to_png_pvr(temp_ktx, output_path):
            return None

        return output_path
    finally:
        await safe_delete(temp_ktx)

async def process_bpc_file(file_name, message: types.Message, r, temp_dir):
    try:
        file_path = os.path.join(temp_dir, file_name)

        decrypted_file = os.path.join(temp_dir, "decrypted_file")
        encrypted = read_file_bytes(file_path)
        xor_key = detect_key_pattern(encrypted)

        decrypted = bytearray()
        for i in range(len(encrypted)):
            decrypted.append(encrypted[i] ^ xor_key[i % len(xor_key)])

        write_bytes_to_file(decrypted_file, decrypted)

        if zipfile.is_zipfile(decrypted_file):
            content_dir = os.path.join(temp_dir, "content")
            os.makedirs(content_dir, exist_ok=True)

            with zipfile.ZipFile(decrypted_file, 'r') as zip_ref:
                zip_ref.extractall(content_dir)

            zip_filename = f"{r}_common.zip"
            zip_path = os.path.join(temp_dir, zip_filename)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(content_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, content_dir)
                        zipf.write(file_path, arcname)

            name = message.from_user.first_name
            await message.answer_document(
                FSInputFile(zip_path), caption='<b>⚡️Ваш файл готов!</b>', parse_mode='HTML')
            name = message.from_user.first_name
        else:
            await message.answer_document(
                FSInputFile(decrypted_file), caption='<b>⚡️Ваш файл готов!</b>', parse_mode='HTML')

    finally:
        if os.path.exists(temp_dir):
            rmtree(temp_dir, ignore_errors=True)


async def process_zip_file(file_name, message: types.Message, r, temp_dir):

    file_path = os.path.join(temp_dir, file_name)

    encrypted_file = os.path.join(temp_dir, f"{r}_common.bpc")
    original_data = read_file_bytes(file_path)
    xor_key = bytes.fromhex('31 63 4b 31 61 35 55 46 32 74 55 38 2a 47 32 6c 57 23 26 25')

    encrypted = bytearray()
    for i in range(len(original_data)):
        encrypted.append(original_data[i] ^ xor_key[i % len(xor_key)])

    write_bytes_to_file(encrypted_file, encrypted)
    await message.answer_document(
        FSInputFile(encrypted_file), caption='<b>⚡️Ваш файл готов!</b>', parse_mode='HTML')


def read_file_bytes(file_path):
    with open(file_path, 'rb') as f:
        return bytearray(f.read())


def write_bytes_to_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)


def detect_key_pattern(encrypted_data):
    signatures = {
        'ZIP': b'PK',
        'PNG': b'\x89PNG',
        'JPEG': b'\xFF\xD8\xFF',
        'GIF': b'GIF',
        'PDF': b'%PDF'
    }

    for key_len in [20, 16, 32, 8, 4]:
        test_key = bytearray()
        for i in range(key_len):
            for sig_type, sig_bytes in signatures.items():
                if i < len(sig_bytes):
                    test_key.append(encrypted_data[i] ^ sig_bytes[i])

        if test_key:
            test_decrypted = bytes([encrypted_data[i] ^ test_key[i % len(test_key)]
                                    for i in range(min(100, len(encrypted_data)))])

            for sig_type, sig_bytes in signatures.items():
                if test_decrypted.startswith(sig_bytes):
                    return test_key

    return bytes.fromhex('31 63 4b 31 61 35 55 46 32 74 55 38 2a 47 32 6c 57 23 26 25')


def is_valid_filename(filename):
    pattern = r'(common|pweper\.common|common\s*\(\d+\))'
    return (
            re.search(pattern, filename, re.IGNORECASE) is not None and
            filename.lower().endswith(('.zip', '.bpc'))
    )


async def handle_valid_files(message: types.Message, ):
    name = message.from_user.first_name

    progress_msg = await message.reply(f"<b>⏳ Обрабатываю ваш файл...</b>", parse_mode="HTML")

    try:
        if message.document.file_name.lower().endswith('.bpc'):
            await process_bpc_file(message.document, message)
    except Exception as e:
        name = message.from_user.first_name
        await progress_msg.edit_text(f"<b>Произошла ошибка: {str(e)}</b>")
    finally:
        try:
            await progress_msg.delete()
        except:
            pass

def rgb_to_hex(rgb):
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'


def process_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: Не удалось декодировать JSON из файла '{filename}'.")
        return
    colors_to_find = [
        "SkyBottomRGB",
        "SkyTopRGB",
        "CloudRGB",
        "SunCoreRGB"
    ]

    found_colors = {}
    for key in colors_to_find:
        if key in data:
            rgb_values = data[key]
            if isinstance(rgb_values, list) and len(rgb_values) == 3:
                hex_value = rgb_to_hex(rgb_values)
                found_colors[key] = hex_value
            else:
                print(f"Предупреждение: Неверный формат данных для ключа '{key}'. Ожидается список из 3 чисел.")
        else:
            print(f"Предупреждение: Ключ '{key}' не найден в JSON файле.")
    for key, hex_value in found_colors.items():
        i = i + f"{key}: {hex_value}"
    return i

def search_in_skins(query: str):
    results = []
    try:
        with open('Editing/skins.txt', 'r', encoding='utf-8') as file:
            current_id = None
            current_name = None

            for line in file:
                line = line.strip()
                if line.startswith("ID - "):
                    current_id = line[5:]
                elif line.startswith("NAME - "):
                    current_name = line[7:]

                    if current_id and current_name:
                        if query == current_id:
                            return [(current_id, current_name)]

                        clean_query = query.lower().replace('.mod', '')
                        mod_name = current_name.lower().replace('.mod', '')

                        if clean_query in mod_name:
                            results.append((current_id, current_name))

                        current_id = None
                        current_name = None

    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    return results


async def file(id_xyina: str, name_xyina: str, message):
    mod_name = name_xyina.replace('.mod', '').lower()

    dff_path = os.path.join('Editing', 'mod', f"{mod_name}.mod")
    dff_file = None
    if os.path.exists(dff_path):
        dff_file = FSInputFile(dff_path)

    zip_path = os.path.join('Editing', 'texture', f"texture_{mod_name}.zip")
    zip_file = None
    if os.path.exists(zip_path):
        zip_file = FSInputFile(zip_path)

    media_group = []
    text_parts = []

    if dff_file:
        media_group.append(InputMediaDocument(media=dff_file))
        text_parts.append(f"{mod_name}.mod")

    if zip_file:
        if media_group:
            media_group.append(InputMediaDocument(media=zip_file, caption=f"ID - {id_xyina}\nNAME - {name_xyina}"))
        else:
            media_group.append(InputMediaDocument(media=zip_file, caption=f"ID - {id_xyina}\nNAME - {name_xyina}"))
        text_parts.append(f"texture_{mod_name}.zip")

    if media_group:
        await message.answer_media_group(media=media_group)

    return text_parts

def assemble_image_from_zip_bytes(zip_bytes, name):
    scale_factor = 1.275

    # Обновленные точные координаты, измеренные по исходному изображению, с учетом масштабирования:
    positions_map = {
        'hud_back.png': (450, 240),  # Большой круг справа
        'hud_up.png': (40, 150),  # Верхний левый прямоугольник ($)
        'hud_center.png': (40, 290),  # Средний левый прямоугольник (сердечки)
        'hud_down.png': (40, 490),  # Нижний средний левый прямоугольник
        'hud_menu.png': (40, 770),  # Нижняя левая кнопка MENU
        'hud_donat_store.png': (520, 770)  # Нижняя правая кнопка/квадрат ($)
    }
    output_size = (1000, 1000)
    assembled_img = Image.new('RGBA', output_size, (0, 0, 0, 0))
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
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
    assembled_img.save(name, format='PNG')

def process_image_sync(file):
    img = Image.open(file).convert("RGBA")
    data = np.array(img)
    alpha = data[:, :, 3]
    kernel_disk = disk(2)
    hist = np.histogram(alpha, bins=256)[0]
    otsu_thresh = exposure.is_low_contrast(
        alpha)
    binary = (alpha > 0).astype(np.uint8) * 255
    from skimage.filters import threshold_otsu
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
    min_pixels = 500
    padding = 10
    for props in regions:
        area = props.area
        if area < min_pixels:
            continue
        y1, x1, y2, x2 = props.bbox
        x1_pad = max(0, x1 - padding)
        y1_pad = max(0, y1 - padding)
        x2_pad = min(data.shape[1], x2 + padding)
        y2_pad = min(data.shape[0], y2 + padding)
        object_img_data = data[y1_pad:y2_pad, x1_pad:x2_pad, :3]
        relative_labels_slice = labels[y1_pad:y2_pad, x1_pad:x2_pad]
        object_mask_bool = (relative_labels_slice == props.label)
        object_mask_closed_bool = closing(object_mask_bool, kernel_disk)
        object_mask = object_mask_closed_bool.astype(np.uint8) * 255
        object_img = np.zeros((y2_pad - y1_pad, x2_pad - x1_pad, 4), dtype=np.uint8)
        object_img[:, :, :3] = object_img_data
        object_img[:, :, 3] = object_mask
        objects.append((area, object_img))
    objects.sort(reverse=True, key=lambda x: x[0])
    if len(objects) == 6:
        prefixes = ['hud_back', 'hud_down', 'hud_up', 'hud_center', 'hud_menu', 'hud_donat_store']
    elif len(objects) == 5:
        prefixes = ['hud_down', 'hud_up', 'hud_center', 'hud_menu', 'hud_donat_store']
    else:
        prefixes = [f'hud_part_{i + 1}' for i in range(len(objects))]
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

def create_and_zip_files(base_src_path, output_dir, zip_name, file_format, name, file_SUFFIXES ):
    zip_path = os.path.join(output_dir, f"{zip_name}_{name}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for suffix in file_SUFFIXES:
            arcname = f"{suffix}.{file_format}"
            archive.write(base_src_path, arcname)
    if os.path.getsize(zip_path) >= MAX_FILE_SIZE:
        os.remove(zip_path)
        return False, None
    return True, zip_path
def prepare_image(src_path):
    img = Image.open(src_path)
    img.close()
    return True
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

async def colorcyc(r, b, g):
    with open('BASEcolorcycle.dat', 'r') as f:
        template_data = f.read()
    final_data = template_data.replace("r", r).replace("g", g).replace("b", b)
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for _ in range(length))
    grn1 = f"{rand_string}_colorcycle.dat"
    with open(grn1, 'w') as f:
        f.write(final_data)
    return grn1
async def timecyc(j):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    output_file_path = f"{rand_string}_timecyc.json"
    with open("main.json", "r", encoding='utf-8') as f:
        timecyc_json_string = f.read()
    replacements = [
        ('"SkyBottomRGB":[SBR016', f'"SkyBottomRGB":{list(ImageColor.getrgb(j[1]))}'),
        ('"SkyTopRGB":[STR016', f'"SkyTopRGB":{list(ImageColor.getrgb(j[2]))}'),
        ('"CloudRGB":[CLR016', f'"CloudRGB":{list(ImageColor.getrgb(j[3]))}'),
        ('"SunCoreRGB":[SCR016', f'"SunCoreRGB":{list(ImageColor.getrgb(j[4]))}')
    ]
    for old_text, new_text in replacements:
        timecyc_json_string = timecyc_json_string.replace(old_text, new_text)
    with open(output_file_path, "w", encoding='utf-8') as f:
        f.write(timecyc_json_string)
    return output_file_path
async def kvadratik(hex_color):
    FONT = ImageFont.truetype("arial.ttf", 24)
    img_width = 400
    img_height = 500
    background_color_rgb = (128, 128, 128)
    image = Image.new("RGB", (img_width, img_height), background_color_rgb)
    draw = ImageDraw.Draw(image)
    rect_width = 200
    rect_height = 200
    rect_x = (img_width - rect_width) // 2
    rect_y = 150
    radius = 20
    hex_color_val = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color_val[i:i + 2], 16) for i in (0, 2, 4))
    draw.rounded_rectangle([(rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height)], radius, fill=rgb_color,outline=(0, 0, 0), width=2)
    text = hex_color
    text_color = (0, 0, 0) if sum(rgb_color) > 384 else (255, 255, 255)
    bbox = draw.textbbox((0, 0), text, font=FONT)
    text_width = bbox[2] - bbox[0]
    text_x = (img_width - text_width) // 2
    text_y = rect_y + rect_height + 20
    draw.text((text_x, text_y), text, font=FONT, fill=text_color)
    image_path = f"color_image_{hex_color.replace('#', '')}.png"
    image.save(image_path)
    return image_path
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            sub TEXT DEFAULT 'False',
            admin TEXT DEFAULT 'False',
            time TEXT -- Дата хранится в формате ISO string (YYYY-MM-DD)
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()
async def save_workbook_to_disk():
    print(f"Изменения в БД сохранены.")

async def update(chat_id, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_date = datetime.datetime.now().date()
    message_to_send = None
    sub = False
    cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    user = cursor.fetchone()

    if user:
        db_chat_id, db_username, db_sub_status, db_admin_status, db_expiration_date_str = user
        if db_expiration_date_str:
            expiration_date = datetime.datetime.strptime(db_expiration_date_str, "%d.%m.%Y").date()
            if expiration_date <= current_date:
                sub = True
                cursor.execute("UPDATE users SET sub='False', time=NULL WHERE chat_id=?", (chat_id,))
                message_to_send = "Ваша подписка закончилась!"
        if db_username != username:
            cursor.execute("UPDATE users SET username=? WHERE chat_id=?", (username, chat_id))

    else:
        new_user_data = (chat_id, username, "False", "False", None)
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", new_user_data)
        message_to_send = "Вы были успешно добавлены в базу данных!"
    conn.commit()
    conn.close()
    await save_workbook_to_disk()
    return sub, message_to_send

def recolor_image_optimized_sync(image_path_or_bytes, hex_color, alpha=1.0):
    if not (0.0 <= alpha <= 1.0):
        alpha = 1.0
    try:
        new_color_np = np.array(mcolors.to_rgb(hex_color), dtype=np.float32)
    except ValueError:
        logging.warning(f"Invalid hex color: {hex_color}. Using default white.")
        new_color_np = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    if isinstance(image_path_or_bytes, bytes):
        img = Image.open(io.BytesIO(image_path_or_bytes))
    else:
        img = Image.open(image_path_or_bytes)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
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
def sync_process_file_task_optimized(file_path: Path, color_hex, alpha):
    image_bytes = recolor_image_optimized_sync(str(file_path), color_hex, alpha)
    arcname = file_path.name
    return image_bytes, arcname
async def color(color_hex, src_zip_path: Path, original_zip_name: str, alpha=1.0):
    r = generate_random_string(length)
    work_dir = Path(f'work/work_HUD/{r}')
    await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
    await asyncio.to_thread( zipfile.ZipFile(src_zip_path, 'r').extractall, work_dir)
    files_to_process = []
    for file in work_dir.glob('*'):
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            files_to_process.append(file)
    tasks = [asyncio.to_thread(sync_process_file_task_optimized, file, color_hex, alpha)
        for file in files_to_process]
    processed_files_info = await asyncio.gather(*tasks)
    output_zip_dir = Path(f'work/work_HUD/{r}')
    await asyncio.to_thread(os.makedirs, output_zip_dir, exist_ok=True)
    output_zip_path = output_zip_dir / f'{original_zip_name}_recolored_{r}.zip'
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        for image_bytes, arcname in processed_files_info:
            f.writestr(arcname, image_bytes)
    return output_zip_dir, output_zip_path


def _process_image_bytes(image_bytes, color_hex, alpha):
    if not (0.0 <= alpha <= 1.0):
        alpha = 1.0
    try:
        new_color_np = np.array(mcolors.to_rgb(color_hex), dtype=np.float32)
    except ValueError:
        logging.warning(f"Invalid hex color: {color_hex}. Using default white.")
        new_color_np = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
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
async def color_optimized(color_hex, src_zip_path: Path, original_zip_name: str, alpha=1.0):
    r = generate_random_string(4)
    files_to_process = []
    with zipfile.ZipFile(src_zip_path, 'r') as src_zip:
        for zip_info in src_zip.infolist():
            if not zip_info.is_dir() and zip_info.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                files_to_process.append((zip_info.filename, src_zip.read(zip_info.filename)))
    loop = asyncio.get_running_loop()
    tasks = []
    with ThreadPoolExecutor() as executor:
        for filename, image_bytes in files_to_process:
            task = loop.run_in_executor(
                executor,
                _process_image_bytes,
                image_bytes,
                color_hex,
                alpha
            )
            tasks.append((filename, task))
        processed_files_info = []
        for filename, task in tasks:
            result_bytes = await task
            if result_bytes is not None:
                processed_files_info.append((result_bytes, filename))
            else:
                logging.warning(f"Skipping file {filename} due to processing error.")
    output_zip_dir = Path(f'work/work_HUD/{r}')
    work_dir = Path(f'work/work_HUD/{r}')
    await asyncio.to_thread(os.makedirs, output_zip_dir, exist_ok=True)
    output_zip_path = output_zip_dir / f'{original_zip_name}_recolored_{r}.zip'
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        for image_bytes, arcname in processed_files_info:
            f.writestr(arcname, image_bytes)
    logging.info(f"Created output zip: {output_zip_path}")
    return output_zip_dir, output_zip_path

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


async def setup_work_dirs():
    work_dirs = ['work/', 'work/work_MAP/', 'work/work_BILD/', 'work/work_BLOOD/',
                 'work/work_LOGO/', 'work/work_TREE/', 'work/work_COLOR/',
                 'work/work_BTX/', 'work/work_TXD/', 'work/work_BPC/',
                 'work/work_HUD/', 'work/work_ANI/', 'work/work_COMPRESS', 'work/work_COL', 'work/work_MOD']
    for d in work_dirs:
        os.makedirs(d, exist_ok=True)


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
def parse_caption(caption):
    parts = caption.split()
    if '/color' not in parts:
        return None, None, None
    try:
        hex_color = parts[1]
        if not hex_color.startswith('#'):
            hex_color = '#' + hex_color
    except IndexError:
        return None, None, None
    alpha = 1.0
    try:
        if len(parts) > 2:
            alpha = float(parts[2])
    except ValueError:
        pass
    return hex_color, alpha

def parse_text(text):
    parts = text.split()
    if '/color' not in parts:
        return None, None
    try:
        hex_color = parts[1]
        if not hex_color.startswith('#'):
            hex_color = '#' + hex_color
    except IndexError:
        return None, None
    alpha = 1.0
    try:
        if len(parts) > 2:
            alpha = float(parts[2])
    except ValueError:
        pass
    return hex_color, alpha

def parse_filter(caption):
    parts = caption.split()
    if '/filters' not in parts:
        return None, None, None
    try:
        filter = parts[1]
    except IndexError:
        return None, None, None
    return filter

def find_user_data_in_sql(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sub, time FROM users WHERE chat_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        db_sub_status_str, db_expiration_date_str = result
        is_subscribed = db_sub_status_str == 'True'
        return is_subscribed, db_expiration_date_str
    else:
        return False, None
async def get_user_status_async(user_id):
    return await asyncio.to_thread(find_user_data_in_sql, user_id)


def apply_filter_on_bytes_optimized(image_bytes: bytes, filter_name: str):
    img_pil = Image.open(io.BytesIO(image_bytes))
    if img_pil.mode != 'RGBA':
        img_pil = img_pil.convert('RGBA')
    img_arr = np.array(img_pil)
    rgb_channels = img_arr[:, :, :3]
    alpha_channel = img_arr[:, :, 3]
    filtered_rgb = None
    filter_name = filter_name.lower()
    enhancement_factor = 1.5
    if filter_name == 'red':
        temp_r = rgb_channels[:, :, 0].astype(np.uint16) * enhancement_factor
        rgb_channels[:, :, 0] = np.clip(temp_r, 0, 255).astype(np.uint8)
        filtered_rgb = rgb_channels
    elif filter_name == 'green':
        temp_g = rgb_channels[:, :, 1].astype(np.uint16) * enhancement_factor
        rgb_channels[:, :, 1] = np.clip(temp_g, 0, 255).astype(np.uint8)
        filtered_rgb = rgb_channels
    elif filter_name == 'blue':
        temp_b = rgb_channels[:, :, 2].astype(np.uint16) * enhancement_factor
        rgb_channels[:, :, 2] = np.clip(temp_b, 0, 255).astype(np.uint8)
        filtered_rgb = rgb_channels
    elif filter_name == 'grayscale':
        grayscale_2d = np.dot(rgb_channels[..., :3], [0.2989, 0.5870, 0.1140])
        filtered_rgb = np.repeat(grayscale_2d[:, :, np.newaxis], 3, axis=2)
        filtered_rgb = np.clip(filtered_rgb, 0, 255).astype(np.uint8)
    elif filter_name == 'negate':
        filtered_rgb = 255 - rgb_channels
    elif filter_name == 'sepia':
        sepia_matrix = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]).T
        rgb_float = rgb_channels.astype(np.float32) / 255.0
        filtered_rgb_float = np.dot(rgb_float, sepia_matrix.T)  # Note the transpose change due to numpy stacking
        filtered_rgb = np.clip(filtered_rgb_float * 255.0, 0, 255).astype(np.uint8)
    elif filter_name == 'solarize':
        threshold = 128
        mask = rgb_channels > threshold
        filtered_rgb = rgb_channels.copy()
        filtered_rgb[mask] = 255 - filtered_rgb[mask]
    else:
        raise ValueError(f"Неизвестный или неподдерживаемый фильтр: '{filter_name}'")
    final_img_arr = np.dstack([
        filtered_rgb,
        alpha_channel
    ])
    final_img_pil = Image.fromarray(final_img_arr, 'RGBA')
    with io.BytesIO() as img_buffer:
        final_img_pil.save(img_buffer, format='PNG')
        return img_buffer.getvalue()

def sync_process_file_filter_task(file_path: Path, filter_name: str):
    with open(file_path, 'rb') as f:
        image_bytes_original = f.read()
    image_bytes_processed = apply_filter_on_bytes_optimized(image_bytes_original, filter_name)
    arcname = file_path.name
    return image_bytes_processed, arcname
async def filter_zip(filter_name: str, src_zip_path: Path, original_zip_name: str):
    r = generate_random_string(length)
    work_dir = Path(f'work/work_filter_{r}')
    await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
    await asyncio.to_thread(zipfile.ZipFile(src_zip_path, 'r').extractall, work_dir)
    files_to_process = []
    for file in work_dir.glob('*'):
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            files_to_process.append(file)
    tasks = [
        asyncio.to_thread(sync_process_file_filter_task, file, filter_name)
        for file in files_to_process
    ]
    processed_files_info = await asyncio.gather(*tasks)
    output_zip_dir = Path(f'work/output_zips/')
    await asyncio.to_thread(os.makedirs, output_zip_dir, exist_ok=True)
    output_zip_path = output_zip_dir / f'{original_zip_name}_filtered_{filter_name}_{r}.zip'
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        for image_bytes, arcname in processed_files_info:
            f.writestr(arcname, image_bytes)
    await asyncio.to_thread(shutil.rmtree, work_dir)
    return output_zip_path


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Неверный формат шестнадцатеричного цвета")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
def _apply_recolor_to_bytes(image_bytes, target_hex_color, replacement_hex_color, tolerance=10):
    try:
        target_rgb_tuple = hex_to_rgb(target_hex_color)
        replacement_rgb_tuple = hex_to_rgb(replacement_hex_color)
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img_np = np.array(img, dtype=np.uint8)
        rgb_channels = img_np[:, :, :3]
        alpha_channel = img_np[:, :, 3]
        target_np = np.array(target_rgb_tuple, dtype=np.uint8)
        color_match_mask = np.all(np.abs(rgb_channels.astype(int) - target_np.astype(int)) <= tolerance, axis=-1)
        rgb_channels[color_match_mask] = replacement_rgb_tuple
        final_img_np = np.concatenate([rgb_channels, alpha_channel[:, :, np.newaxis]], axis=2)
        new_img = Image.fromarray(final_img_np, 'RGBA')
        buffer = io.BytesIO()
        new_img.save(buffer, format="PNG")
        return buffer.getvalue()
    except ValueError as ve:
        logging.error(f"Ошибка параметров цвета: {ve}")
        return None
    except Exception as e:
        logging.error(f"Ошибка обработки изображения: {e}")
        return None
def parse_recolor_command(caption):
    parts = caption.split()
    if len(parts) < 3 or len(parts) > 4:
        return None
    target_hex = parts[1]
    replacement_hex = parts[2]
    tolerance = 10
    if len(parts) == 4:
        try:
            tolerance = int(parts[3])
            if not (0 <= tolerance <= 255):
                logging.warning("Допуск вне диапазона [0, 255]")
                return None
        except ValueError:
            logging.warning("Неверный формат допуска (должно быть целое число)")
            return None
    if not (target_hex.startswith('#') and len(target_hex) == 7 and
            replacement_hex.startswith('#') and len(replacement_hex) == 7):
        logging.warning("Неверный формат hex-цвета (ожидается #RRGGBB)")
        return None
    return target_hex, replacement_hex, tolerance

def process_aim_image_optimized(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    new_img = Image.new("RGBA", (img.width * 2, img.height * 2))
    new_img.paste(img, (0, 0))
    new_img.paste(img.rotate(90), (0, img.height))
    new_img.paste(img.rotate(180), (img.width, img.height))
    new_img.paste(img.rotate(270), (img.width, 0))
    buffer = io.BytesIO()
    new_img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()

async def recolor_zip_optimized(target_hex, replacement_hex, tolerance, src_zip_path: Path):
    target_rgb_tuple = tuple(int(target_hex.strip('#')[i:i + 2], 16) for i in (0, 2, 4))
    replacement_rgb_tuple = tuple(int(replacement_hex.strip('#')[i:i + 2], 16) for i in (0, 2, 4))
    files_to_process = []
    with zipfile.ZipFile(src_zip_path, 'r') as src_zip:
        for zip_info in src_zip.infolist():
            if not zip_info.is_dir() and zip_info.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                files_to_process.append((zip_info.filename, src_zip.read(zip_info.filename)))
    loop = asyncio.get_running_loop()
    processed_files_info = []
    with ThreadPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor,_apply_recolor_to_bytes,image_bytes,target_rgb_tuple,replacement_rgb_tuple,tolerance)
            for filename, image_bytes in files_to_process]
        results = await asyncio.gather(*tasks)
        for i, result_bytes in enumerate(results):
            if result_bytes is not None:
                processed_files_info.append((result_bytes, files_to_process[i][0]))
    buffer_out = io.BytesIO()
    with zipfile.ZipFile(buffer_out, 'w', compression=zipfile.ZIP_DEFLATED) as f_out:
        for image_bytes_result, arcname in processed_files_info:
            f_out.writestr(arcname, image_bytes_result)
    buffer_out.seek(0)
    return buffer_out.getvalue()

def generate_random_string(length=4):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
def parse_caption_for_compression(caption: str) -> tuple[int, int]:
    try:
        parts = caption.split()
        size_str = next((p for p in parts if 'x' in p), None)
        if not size_str:
            return None, None
        width, height = map(int, size_str.split('x'))
        return width, height
    except ValueError:
        return None, None

def _compress_image_bytes_sync(image_bytes: bytes, target_size: tuple[int, int], original_format: str) -> tuple[bytes, str]:
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()

            if original_format.lower() == 'png' and img.mode in ('RGBA', 'P'):
                img.save(output_buffer, format='PNG', optimize=True)
                return output_buffer.getvalue(), 'png'
            else:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_buffer, format='JPEG', optimize=True, quality=85)
                return output_buffer.getvalue(), 'jpg'
    except Exception as e:
        print(f"Error during image processing: {e}")
        return b"", ""
def _process_zip_sync(download_path: Path, output_zip_path: Path, target_size: tuple[int, int]):
    with open(download_path, 'rb') as f:
        input_zip_bytes = f.read()
    output_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(input_zip_bytes), 'r') as input_zip:
        with zipfile.ZipFile(output_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as output_zip:
            for filename in input_zip.namelist():
                file_format = filename.split('.')[-1].lower()
                if file_format in ("png", "jpg", "jpeg"):
                    try:
                        image_bytes = input_zip.read(filename)
                        processed_bytes, new_format = _compress_image_bytes_sync(image_bytes, target_size, file_format)
                        new_filename = Path(filename).stem + f'.{new_format}'
                        output_zip.writestr(new_filename, processed_bytes)
                    except Exception as e:
                        print(f"Could not process {filename}: {e}")
                        output_zip.writestr(filename, image_bytes)
                else:
                    output_zip.writestr(filename, input_zip.read(filename))

    with open(output_zip_path, 'wb') as f:
        f.write(output_zip_buffer.getvalue())

@dp.message(F.document)
async def handle_document_processing(message: types.Message):
    letters = string.ascii_lowercase
    r = ''.join(random.choice(letters) for i in range(length))
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"
    caption = message.caption or ''
    file_name = message.document.file_name
    file_format = file_name.split('.')[1]
    sub, message_to_send = await update(user_id, username)
    if sub:
        await message.answer(message_to_send)
        return
    is_subscribed, expiry_date_value = await get_user_status_async(user_id)
    if not is_subscribed:
        await message.answer(NOT_HI_MESSAGE)
        return
    if 'boti' in globals() and 'loging_id' in globals():
        log_message = (f"[{datetime.datetime.now()}] @{username} ({user_id}) "
            f"Отправил файл - {file_name} с подписью: {caption}")
        for chat_id in loging_id:
            await boti.send_message(chat_id, log_message)
    if '/color' in caption:
        hex_color, alpha = parse_caption(caption)
        if not hex_color:
            await message.answer("❔ Пример использования: `/color #FF0000 0.4`\n"
                "Цвет должен быть в HEX (например, #RRGGBB)! Альфа не обязательна",parse_mode='Markdown')
            return
        processing_message = await message.answer("Обрабатываю...")
        src_dir = Path(f'work/work_COLOR/{r}')
        await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
        download_path = src_dir / file_name
        if file_format in ["jpeg", "jpg", "png"]:
            image_bytes_original = io.BytesIO()
            await bot.download(file=message.document.file_id, destination=image_bytes_original)
            processed_bytes = await asyncio.to_thread(_process_image_bytes, image_bytes_original.getvalue(),hex_color, alpha)
            f = types.BufferedInputFile(processed_bytes, filename=f"recolored_{file_name}")
            await message.answer_document(f, caption='<b>⚡️Файл готов!</b>', parse_mode='HTML')
        elif file_format == "zip":
            await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
            await bot.download(file=message.document.file_id, destination=download_path)
            file_name2 = download_path.stem
            work_dir_parent, output_zip_path = await color_optimized(hex_color, download_path, file_name2, alpha)
            f = FSInputFile(str(output_zip_path))
            await processing_message.delete()
            await bot.send_document(message.chat.id, f, caption='<b>⚡️Файл готов!</b>', parse_mode='HTML')
            await asyncio.to_thread(os.remove, output_zip_path)
        else:
            await message.answer(f"❔ Неподдерживаемый формат файла: .{file_format}")
        if src_dir.exists():
            await asyncio.to_thread(shutil.rmtree, src_dir)
    elif '/filters' in caption:
        filter = parse_filter(caption)
        if not filter:
            await message.answer("❔ Пример использования: `/filters red`\n"
                "-➤ Фильтры:\n└ red — усиление красного канала\n└ green — усиление зеленого канала\n└ blue — усиление синего канала\n└ grayscale — применение эффекта чёрно - белой палитры\n└ negate — создание эффекта негатива\n└ sepia — добавление теплого сепийного тона\n└ solarize — эффект передержки изображения",parse_mode='Markdown')
            return
        processing_message = await message.answer("Обрабатываю...")
        src_dir = Path(f'work/work_COLOR/{r}')
        await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
        download_path = src_dir / file_name
        if file_format in ["jpeg", "jpg", "png"]:
            image_bytes_original = io.BytesIO()
            await bot.download(file=message.document.file_id, destination=image_bytes_original)
            processed_bytes = await asyncio.to_thread(apply_filter_on_bytes_optimized, image_bytes_original.getvalue(), filter)
            f = types.BufferedInputFile(processed_bytes, filename=f"filtered_{file_name}")
            await message.answer_document(f, caption='<b>⚡️Файл готов!</b>', parse_mode='HTML')
        elif file_format == "zip":
            await bot.download(file=message.document.file_id, destination=download_path)
            file_name_stem = download_path.stem
            output_zip_path = await filter_zip(filter, download_path, file_name_stem)
            f = FSInputFile(str(output_zip_path))
            await processing_message.delete()
            await bot.send_document(message.chat.id, f,caption=f'<b>⚡️ZIP с фильтром "{filter}" готов!</b>', parse_mode='HTML')
            await asyncio.to_thread(os.remove, download_path)
            await asyncio.to_thread(os.remove, output_zip_path)
            await asyncio.to_thread(shutil.rmtree, src_dir)
        else:
            await message.answer(f"❔ Неподдерживаемый формат файла: .{file_format}")
    elif '/recolor' in caption:
        recolor_params = parse_recolor_command(caption)
        if not recolor_params:
            await message.answer("❔ Пример: `/recolor #ffbbbb #661717 30`", parse_mode='Markdown')
            return
        target_hex, replacement_hex, tolerance = recolor_params
        processing_message = await message.answer("Обрабатываю перекраску...")
        try:
            if file_format in ["jpeg", "jpg", "png"]:
                image_bytes_original = io.BytesIO()
                await bot.download(file=message.document.file_id, destination=image_bytes_original)
                processed_bytes = await asyncio.to_thread(_apply_recolor_to_bytes,image_bytes_original.getvalue(),target_hex,replacement_hex,tolerance)
                if processed_bytes:
                    f = BufferedInputFile(processed_bytes, filename=f"recolored_{file_name}")
                    await message.answer_document(f, caption='<b>⚡️Файл готов!</b>', parse_mode='HTML')
                else:
                    await message.answer("Произошла ошибка при обработке изображения.")

            elif file_format == "zip":
                download_path = Path(f'work/temp_downloads/src_{r}.zip')
                await asyncio.to_thread(os.makedirs, download_path.parent, exist_ok=True)
                await bot.download(file=message.document.file_id, destination=download_path)
                zip_bytes_result = await recolor_zip_optimized(target_hex, replacement_hex, tolerance, download_path)
                output_zip_path = Path(f'work/temp_downloads/out_{r}.zip')
                await asyncio.to_thread(output_zip_path.write_bytes, zip_bytes_result)
                f = FSInputFile(str(output_zip_path))
                await processing_message.delete()
                await bot.send_document(message.chat.id, f, caption=f'<b>⚡️ZIP с перекраской готов!</b>', parse_mode='HTML')
                await asyncio.to_thread(os.remove, download_path)
                await asyncio.to_thread(os.remove, output_zip_path)
            else:
                await message.answer(f"❔ Неподдерживаемый формат файла: .{file_format}")
        except Exception as e:
            logging.exception("An error occurred during recolor process")
            await message.answer(f"Произошла непредвиденная ошибка: {e}")
        finally:
            try:
                await processing_message.delete()
            except Exception:
                pass
    elif '/aim' in caption:
        if file_format not in ["png", "jpg", "jpeg"]:
            await message.answer(f"❔ Неподдерживаемый формат файла: .{file_format}")
            return
        processing_message = await message.answer("Обрабатываю...")
        try:
            image_bytes_original = io.BytesIO()
            await bot.download(file=message.document.file_id, destination=image_bytes_original)
            processed_bytes = await asyncio.to_thread(process_aim_image_optimized, image_bytes_original.getvalue())
            f = BufferedInputFile(processed_bytes, filename=f"aim_{file_name}")
            await bot.send_document(message.chat.id, f, caption=f'<b>⚡️Прицел готов!</b>', parse_mode='HTML')
        except Exception as e:
            logging.exception("An error occurred during /aim processing")
            await message.answer(f"Произошла ошибка при обработке: {e}")
        finally:
            await processing_message.delete()
    elif '/compress' in caption:
        if message.document:
            file_name = message.document.file_name
            file_format = file_name.split('.')[-1].lower()
            file_id = message.document.file_id
        else:
            await message.answer("Пожалуйста, отправьте файл документом.")
            return
        width, height = parse_caption_for_compression(caption)
        if not width:
            await message.answer("Ошибка парсинга размера.")
            return
        target_size = (width, height)
        processing_message = await message.answer(f"Обрабатываю сжатие до {width}x{height}...",parse_mode='Markdown')
        src_dir = Path(f'work/work_COMPRESS/{r}')
        await asyncio.to_thread(os.makedirs, src_dir, exist_ok=True)
        download_path = src_dir / file_name
        if file_format in ["jpeg", "jpg", "png"]:
            image_bytes_original = io.BytesIO()
            await bot.download(file=message.document.file_id, destination=image_bytes_original)
            processed_bytes, new_format = await asyncio.to_thread(_compress_image_bytes_sync, image_bytes_original.getvalue(),target_size,file_format)
            original_stem = Path(file_name).stem
            final_filename = f"compressed_{original_stem}.{new_format}"
            f = types.BufferedInputFile(processed_bytes, filename=final_filename)
            await processing_message.delete()
            await message.answer_document(f, caption='<b>⚡️Файл готов!</b>', parse_mode='HTML')
        elif file_format == "zip":
            await bot.download(file=file_id, destination=download_path)
            file_name_stem = download_path.stem
            output_zip_path = src_dir / f"{file_name_stem}_compressed.zip"
            await asyncio.to_thread(_process_zip_sync, download_path, output_zip_path, target_size)
            f = FSInputFile(str(output_zip_path))
            await processing_message.delete()
            await bot.send_document(message.chat.id, f, caption='<b>⚡️Файл готов!</b>', parse_mode='HTML')
        else:
            await processing_message.delete()
            await message.answer(f"❔ Неподдерживаемый формат файла: .{file_format}")
        if src_dir.exists():
            await asyncio.to_thread(shutil.rmtree, src_dir)
    elif '/logo'  in caption:
        n = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        work_dir = Path(f'work/work_LOGO/{r}')
        await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
        src = os.path.join(work_dir, file_name)
        download_path = work_dir / file_name
        try:
            await bot.download(file=message.document.file_id, destination=download_path)
            file_name_stem = download_path.stem
            y = await message.answer("Обрабатываю...")
            success, zip_path = await asyncio.get_running_loop().run_in_executor(None,create_and_zip_files,src,work_dir,n,file_format, "logo", FILE_SUFFIXES)
            if not success:
                await message.answer("Ваш файл слишком большой!")
                await y.delete()
                return
            await y.delete()
            i = FSInputFile(zip_path)
            await bot.send_document(message.chat.id, i, caption=f'<b>⚡️Ваши логотипы готовы!</b>', parse_mode='HTML')
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
        finally:
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir)
    elif '/tree'  in caption:
        n = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        work_dir = Path(f'work/work_TREE/{r}')
        await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
        src = os.path.join(work_dir, file_name)
        download_path = work_dir / file_name
        try:
            await bot.download(file=message.document.file_id, destination=download_path)
            file_name_stem = download_path.stem
            y = await message.answer("Обрабатываю...")
            success, zip_path = await asyncio.get_running_loop().run_in_executor(None,create_and_zip_files,src,work_dir,n,file_format, "tree", Tree)
            if not success:
                await message.answer("Ваш файл слишком большой!")
                await y.delete()
                return
            await y.delete()
            i = FSInputFile(zip_path)
            await bot.send_document(message.chat.id, i, caption=f'<b>⚡️Ваши деревья готовы!</b>', parse_mode='HTML')
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
        finally:
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir)
    elif '/bild'  in caption:
        n = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        work_dir = Path(f'work/work_BILD/{r}')
        await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
        src = os.path.join(work_dir, file_name)
        download_path = work_dir / file_name
        try:
            await bot.download(file=message.document.file_id, destination=download_path)
            file_name_stem = download_path.stem
            y = await message.answer("Обрабатываю...")
            success, zip_path = await asyncio.get_running_loop().run_in_executor(None,create_and_zip_files,src,work_dir,n,file_format, "bild", bild)
            if not success:
                await message.answer("Ваш файл слишком большой!")
                await y.delete()
                return
            await y.delete()
            i = FSInputFile(zip_path)
            await bot.send_document(message.chat.id, i, caption=f'<b>⚡️Ваши билдборды готовы!</b>', parse_mode='HTML')
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
        finally:
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir)
    elif '/map' in caption:
        if file_format in ["jpeg", "jpg", "png"]:
            y = await message.answer("Обрабатываю...")
            img_buffer = io.BytesIO()
            await bot.download(file=message.document.file_id, destination=img_buffer)
            img = Image.open(img_buffer)
            width, height = img.size
            num_squares_side = 14
            square_width = width // num_squares_side
            square_height = height // num_squares_side
            total_squares = num_squares_side * num_squares_side
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
                for i in range(num_squares_side):
                    for j in range(num_squares_side):
                        left = j * square_width
                        top = i * square_height
                        right = (j + 1) * square_width
                        bottom = (i + 1) * square_height
                        box = (left, top, right, bottom)
                        square = img.crop(box)
                        square_buffer = io.BytesIO()
                        save_format = 'JPEG' if file_format in ['jpeg', 'jpg'] else 'PNG'
                        square.save(square_buffer, format=save_format)
                        square_buffer.seek(0)
                        filename = f"radar{str(i * num_squares_side + j).zfill(2)}.{save_format.lower()}"
                        archive.writestr(filename, square_buffer.getvalue())
            zip_buffer.seek(0)
            file_to_send = BufferedInputFile(file=zip_buffer.getvalue(),filename=f'{r}_radar.zip')
            await y.delete()
            await bot.send_document(chat_id=message.chat.id,document=file_to_send,caption=f'<b>⚡️Ваша карта готова!</b>',parse_mode='HTML')

    elif '/remap' in caption:

        chat_id = message.chat.id
        document = message.document
        if not document.file_name.lower().endswith('.zip'):
            await message.answer("Пожалуйста, загрузите файл с расширением .zip.")
            return
        y = await message.answer("Восстанавливаю изображение... ️")
        work_dir = Path(f'work/work_MAP/{r}')
        await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
        download_path = work_dir / file_name
        await bot.download(file=message.document.file_id, destination=download_path)
        images_dict = {}
        num_squares_side = 14
        total_squares = num_squares_side * num_squares_side
        with zipfile.ZipFile(download_path, 'r') as archive:
            for zipinfo in archive.infolist():
                filename = zipinfo.filename
                if filename.startswith('radar') and (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png')):

                    index_str = filename[5:-4]
                    index = int(index_str.replace(".",""))
                    with archive.open(zipinfo) as file_in_zip:
                        img_data = file_in_zip.read()
                        images_dict[index] = Image.open(io.BytesIO(img_data))
        if len(images_dict) != total_squares:
            await y.delete()
            await message.answer(
                f"Найдено только {len(images_dict)} из {total_squares} необходимых частей в архиве.")
            return
        first_image = next(iter(images_dict.values()))
        square_width, square_height = first_image.size
        total_width = square_width * num_squares_side
        total_height = square_height * num_squares_side
        restored_img = Image.new('RGBA', (total_width, total_height))
        for index in range(total_squares):
            img = images_dict[index]
            i = index // num_squares_side
            j = index % num_squares_side
            left = j * square_width
            top = i * square_height
            restored_img.paste(img, (left, top))
            del images_dict[index]
        jjj = f'work/work_MAP/{r}/restored_radar.png'
        restored_img.save(jjj, format='PNG',quality=95)
        await y.delete()
        photo = FSInputFile(jjj)
        await bot.send_document(chat_id, photo, caption=f'<b>⚡️Твое восстановленное изображение готово!</b>', parse_mode='HTML')
    elif '/hudcut' in caption:
        if file_format not in ["png", "jpg", "jpeg"]:
            await message.answer(f"❔ Неподдерживаемый формат файла: .{file_format}")
            return
        processing_message = await message.answer("Обрабатываю...")
        try:
            image_bytes_original = io.BytesIO()
            await bot.download(file=message.document.file_id, destination=image_bytes_original)
            zip_buffer, count = await asyncio.to_thread(process_image_sync, image_bytes_original)
            f = BufferedInputFile(zip_buffer.getvalue(), filename=f"hudcut_{r}.zip")
            await bot.send_document(message.chat.id, f, caption=f'<b>⚡️Ваш нарезаный худ готов!</b>', parse_mode='HTML')
        except Exception as e:
            logging.exception("Ошибка hudcut")
        finally:
            await processing_message.delete()
    elif '/rehud' in caption:

        chat_id = message.chat.id
        document = message.document
        if not document.file_name.lower().endswith('.zip'):
            await message.answer("Пожалуйста, загрузите файл с расширением .zip.")
            return
        y = await message.answer("Восстанавливаю изображение... ️")
        work_dir = Path(f'work/work_HUD/{r}')
        await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
        download_path = work_dir / file_name
        await bot.download(file=message.document.file_id, destination=download_path)
        await asyncio.to_thread(assemble_image_from_zip_bytes, download_path, f'work/work_HUD/{r}/rehud_{r}.png')
        await y.delete()
        photo = FSInputFile(f'work/work_HUD/{r}/rehud_{r}.png')
        await bot.send_document(chat_id, photo, caption=f'<b>⚡️Твое восстановленное изображение готово!</b>', parse_mode='HTML')
    elif '/genrl' in caption:
        chat_id = message.chat.id
        document = message.document
        if not document.file_name.lower().endswith('.bpc'):
            await message.answer("Пожалуйста, загрузите файл с расширением .bpc.")
            return
        y = await message.answer(f"<b>⏳ Обрабатываю ваш файл...</b>", parse_mode="HTML")
        work_dir = Path(f'work/work_BPC/{r}')
        await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
        file_name = message.document.file_name
        download_path = work_dir / file_name
        await bot.download(file=message.document.file_id, destination=download_path)
        await generate_bpcmeta( download_path, f'work/work_BPC/{r}/{r}_GENERIC.bpcmeta')
        await y.delete()
        photo = FSInputFile(f'work/work_BPC/{r}/{r}_GENERIC.bpcmeta')
        await bot.send_document(chat_id, photo, caption=f'<b>⚡️Твой генрл готов!</b>', parse_mode='HTML')
    elif "/bpc" in caption:
        for id in loging_id:
            await boti.send_message(id,
                                    f"[{datetime.datetime.now()}] @{message.from_user.username} ({message.from_user.id}) Отправил файл - {message.document.file_name} без подписи(обработка ipf)")
        file_name = message.document.file_name
        temp_dir = os.path.join(f"work/work_BPC/{r}")
        os.makedirs(temp_dir, exist_ok=True)
        await bot.download(file=message.document.file_id, destination=f'work/work_BPC/{r}/{file_name}')
        await process_zip_file(file_name, message, r, temp_dir)
    else:
        if file_format == "ifp":
            for id in loging_id:
                await boti.send_message(id,
                                        f"[{datetime.datetime.now()}] @{message.from_user.username} ({message.from_user.id}) Отправил файл - {message.document.file_name} без подписи(обработка ipf)")
            os.mkdir(f'work/work_ANI/{r}')
            ipf_buffer = io.BytesIO()
            file_name = message.document.file_name
            file_name2 = file_name.split(".")[0]
            await bot.download(file=message.document.file_id, destination=ipf_buffer)
            ani_file_path = f'work/work_ANI/{r}/{file_name2}.ani'
            download_path = f'work/work_ANI/{r}/{file_name}'
            with open(download_path, 'wb') as new_file:
                new_file.write(ipf_buffer.getvalue())
            with open(ani_file_path, 'wb') as er:
                er.write(ipf_buffer.getvalue())
            y = await message.answer("Обрабатываю...")
            with open(download_path, 'rb') as f_input, open(ani_file_path, 'wb') as f_output:
                f_input.seek(8)
                byte = f_input.read(8)
                while byte:
                    f_output.write(byte)
                    byte = f_input.read(8)
            async with aiofiles.open(ani_file_path, "rb") as f:
                original_data = await f.read()
                new_data = b'\x41\x4E\x50\x33' + original_data
            with open(ani_file_path, 'wb') as er:
                er.write(new_data)
            f = FSInputFile(f'work/work_ANI/{r}/{file_name2}.ani')
            await y.delete()
            await bot.send_document(message.chat.id, f, caption=f'<b>⚡️Ваша анимация готова!</b>', parse_mode='HTML')
            os.removedirs(f'work/work_ANI/{r}')
        elif file_format == "json":
            work_dir = Path(f'work/temp_downloads/{r}')
            await asyncio.to_thread(os.makedirs, work_dir, exist_ok=True)
            src = os.path.join(work_dir, file_name)
            download_path = work_dir / file_name
            try:
                await bot.download(file=message.document.file_id, destination=download_path)
                y = await message.answer("Обрабатываю...")
                i = await asyncio.get_running_loop().run_in_executor(None, process_json_file, src)
                await y.delete()
                await bot.answer(i)
            except Exception as e:
                await message.answer(f"Произошла ошибка: {e}")
            finally:
                if os.path.exists(work_dir):
                    shutil.rmtree(work_dir)
        elif file_format == "cls":
            for id in loging_id:
                await boti.send_message(id,
                                        f"[{datetime.datetime.now()}] @{message.from_user.username} ({message.from_user.id}) Отправил файл - {message.document.file_name} без подписи(обработка ipf)")
            os.mkdir(f'work/work_COL/{r}')
            ipf_buffer = io.BytesIO()
            file_name = message.document.file_name
            file_name2 = file_name.split(".")[0]
            await bot.download(file=message.document.file_id, destination=ipf_buffer)
            ani_file_path = f'work/work_COL/{r}/{file_name2}.ani'
            download_path = f'work/work_COL/{r}/{file_name}'
            with open(download_path, 'wb') as new_file:
                new_file.write(ipf_buffer.getvalue())
            with open(ani_file_path, 'wb') as er:
                er.write(ipf_buffer.getvalue())
            y = await message.answer("Обрабатываю...")
            with open(download_path, 'rb') as f_input, open(ani_file_path, 'wb') as f_output:
                f_input.seek(4)
                byte = f_input.read(4)
                while byte:
                    f_output.write(byte)
                    byte = f_input.read(4)
            async with aiofiles.open(ani_file_path, "rb") as f:
                original_data = await f.read()
                new_data = b'\x43\x4F\x4C\x33' + original_data
            with open(ani_file_path, 'wb') as er:
                er.write(new_data)
            f = FSInputFile(f'work/work_COL/{r}/{file_name2}.ani')
            await y.delete()
            await bot.send_document(message.chat.id, f, caption='Держи файл!')
            os.removedirs(f'work/work_COL/{r}')
        elif file_format == "bpc":
            for id in loging_id:
                await boti.send_message(id,
                                        f"[{datetime.datetime.now()}] @{message.from_user.username} ({message.from_user.id}) Отправил файл - {message.document.file_name} без подписи(обработка ipf)")
            file_name = message.document.file_name
            temp_dir = os.path.join(f"work/work_BPC/{r}")
            os.makedirs(temp_dir, exist_ok=True)
            await bot.download(file=message.document.file_id, destination=f'work/work_BPC/{r}/{file_name}')
            await process_bpc_file(file_name, message, r, temp_dir)
        elif file_format == "txd":
            txd_converter = TXDConverter()
            y = await message.answer(f"<b>⏳ Обрабатываю ваш файл...</b>", parse_mode="HTML")
            try:
                file_data = io.BytesIO()
                await bot.download(file=message.document.file_id, destination=file_data)
                file_bytes = file_data.getvalue()
                png_files = txd_converter.parse_txd_data(file_bytes)
                if not png_files:
                    await y.edit_text(f"<b>Не удалось извлечь текстуры из файла</b>")
                    return
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for png_file in png_files:
                        zip_file.write(png_file, os.path.basename(png_file))
                zip_buffer.seek(0)
                result = BufferedInputFile(
                    zip_buffer.getvalue(),
                    filename=f"{os.path.splitext(message.document.file_name)[0]}.zip"
                )

                await message.reply_document(
                    result, caption=f'<b>⚡️Ваши файлы готовы!</b>', parse_mode='HTML')
            except Exception as e:
                logging.error(f"TXD processing error: {e}", exc_info=True)
            finally:
                await y.delete()
        elif file_format == "mod":
            y = await message.answer(f"<b>⏳ Обрабатываю ваш файл...</b>", parse_mode="HTML")
            file_name = message.document.file_name
            file_name2 = file_name.split(".")[0]
            download_path = Path(f'work/work_MOD/{r}')
            file_down = f'work/work_MOD/{r}/{file_name}'
            os.makedirs(download_path, exist_ok=True)
            await bot.download(file=message.document.file_id, destination=file_down)
            dff_file_path = f'work/work_MOD/{r}/{file_name2}.dff'
            await convert_one(file_down, download_path)
            result = FSInputFile(dff_file_path)
            await y.delete()
            await bot.send_document(message.chat.id,
                result, caption=f'<b>⚡️Ваша модель готова!</b>', parse_mode='HTML')

        elif file_format in ["btx", "png", "jpg", "jpeg" , "zip"]:
            work_dir = Path(f'work/work_BTX/{r}')
            file_name = message.document.file_name
            file_name2 = Path(file_name).stem
            os.makedirs(work_dir, exist_ok=True)
            src_path = work_dir / file_name
            for user_id in loging_id:
                await boti.send_message(user_id,
                                        f"[{datetime.datetime.now()}] @{message.from_user.username} ({message.from_user.id}) Отправил файл - {file_name} (обработка btx)")

            await bot.download(file=message.document.file_id, destination=src_path)
            y = await message.answer("Обрабатываю...")
            if file_format == "btx":
                output_file_path = await convert_btx_to_png(str(src_path), file_name2, work_dir)
                caption = '<b>⚡️Ваше изображение готово!</b>'

            elif file_format in ("png", "jpg"):
                output_file_path = await convert_png_to_btx(str(src_path), file_name, work_dir)
                caption = '<b>⚡️Ваша текстура готова!</b>'

            elif file_format == "zip":
                with zipfile.ZipFile(src_path, 'r') as zip_ref:
                    zip_ref.extractall(work_dir)
                rand_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
                output_file_path = work_dir / f'{rand_string}_BTX.zip'
                files_to_process = [file for file in work_dir.glob('*') if
                                    file.is_file() and file.name not in (file_name, output_file_path.name)]
                processing_tasks = []
                for file in files_to_process:
                    inner_file_format = file.suffix.lower()
                    inner_file_name2 = file.stem
                    if inner_file_format == ".btx":
                        output_file = processing_tasks.append(convert_btx_to_png(str(file), inner_file_name2, work_dir))
                    elif inner_file_format in (".png", ".jpg"):
                        output_file = processing_tasks.append(convert_png_to_btx(str(file), inner_file_name2, work_dir))
                await asyncio.gather(*processing_tasks)
                with zipfile.ZipFile(output_file_path, 'a') as f_zip_out:
                    for file in work_dir.glob('*'):
                        if file.suffix.lower() in ('.png', '.btx') and file.name != file_name:
                            f_zip_out.write(file, file.name)

                caption = '<b>⚡️Ваши файлы готовы!</b>'
            f = FSInputFile(str(output_file_path))
            await y.delete()
            await bot.send_document(message.chat.id, f, caption=caption, parse_mode='HTML')
            if work_dir.exists():
                shutil.rmtree(work_dir)
        elif file_format == "dat":
            y = await message.answer(f"<b>⏳ Обрабатываю ваш файл...</b>", parse_mode="HTML")
            try:
                file_name = message.document.file_name
                file_name2 = file_name.split(".")[0]
                temp = f'work/work_MOD/{r}'
                os.makedirs(temp, exist_ok=True)
                await bot.download(file=message.document.file_id, destination=temp)
                json_file_path = f'work/work_MOD/{r}/{file_name2}.json'
                json = await convert_timecyc_dat_to_json(json_file_path, file_name, temp)
                result = FSInputFile(json_file_path)
                await message.reply_document(
                    result, caption=f'<b>⚡️Ваша модель готова!</b>', parse_mode='HTML')
            except Exception as e:
                logging.error(f"TXD processing error: {e}", exc_info=True)
            finally:
                await y.delete()

@dp.message(F.text)
async def ok(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    if 'boti' in globals() and 'loging_id' in globals():
        log_message = (
            f"[{datetime.datetime.now()}] @{username} ({user_id}) "
            f"Написал: {message.text}"
        )
        for chat_id in loging_id:
            await boti.send_message(chat_id, log_message)
    sub, message_to_send = await update(user_id, username)
    if sub:
        await message.answer(message_to_send)
        return
    is_subscribed, expiry_date_value = await get_user_status_async(message.from_user.id)
    if not is_subscribed:
        await message.answer(NOT_HI_MESSAGE)
        return
    j = message.text.split()
    if "/start" in message.text:
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(text="Открыть палитру HEX", web_app=types.WebAppInfo(url="https://csscolor.ru")))
        hello = f'<b>👋Привет это бот для создания сборок!</b>\n\n💳Твоя подписка все еще действует до {expiry_date_value}!\n\nКоманды - /help'
        await message.answer(hello, reply_markup=builder.as_markup(), parse_mode='HTML')
    if "/mysub" in message.text:
        hello = f'<b>💳Твоя подписка все еще действует до {expiry_date_value}!</b>'
        await message.answer(hello, parse_mode='HTML')
    if '/hud1' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /hud1 <color> <alpha>\nПример использования: /hud1 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud1.zip", "hud1", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud1.zip", "hud1")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Hud готов!</b>', parse_mode='HTML')
        await asyncio.to_thread(shutil.rmtree, work_dir)

    if '/hud2' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /hud2 <color> <alpha>\nПример использования: /hud2 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud2.zip", "hud2", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud2.zip", "hud2")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Hud готов!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/hud3' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /hud3 <color> <alpha>\nПример использования: /hud3 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud3.zip", "hud3", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud3.zip", "hud3")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Hud готов!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/hud4' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /hud4 <color> <alpha>\nПример использования: /hud4 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud4.zip", "hud4", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hud4.zip", "hud4")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Hud готов!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/hp1' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /hp1 <color> <alpha>\nПример использования: /hp1 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp1.zip", "hp1", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp1.zip", "hp1")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши элементы худа готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/hp2' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /hp2 <color> <alpha>\nПример использования: /hp2 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp2.zip", "hp2", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp2.zip", "hp2")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши элементы худа готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/hp3' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /hp3 <color> <alpha>\nПример использования: /hp3 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp3.zip", "hp3", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/hp3.zip", "hp3")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши элементы худа готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/blood' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /blood <color> <alpha>\nПример использования: /blood #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/blood.zip", "blood", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/blood.zip", "blood")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваша кровь готова!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/tree' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /tree <color> <alpha>\nПример использования: /tree #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/tree.zip", "tree", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/tree.zip", "tree")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши деревья готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/vctree' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /vctree <color> <alpha>\nПример использования: /vctree #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/vctree.zip", "vctree", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/vctree.zip", "vctree")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши деревья готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp1' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp1 <color> <alpha>\nПример использования: /kp1 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp1.zip", "kp1", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp1.zip", "kp1")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp2' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp2 <color> <alpha>\nПример использования: /kp2 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp2.zip", "kp2", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp2.zip", "kp2")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp3' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp3 <color> <alpha>\nПример использования: /kp3 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp3.zip", "kp3", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp3.zip", "kp3")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp4' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp4 <color> <alpha>\nПример использования: /kp4 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp4.zip", "kp4", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp4.zip", "kp4")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp5' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp5 <color> <alpha>\nПример использования: /kp5 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp5.zip", "kp5", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp5.zip", "kp5")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp6' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp6 <color> <alpha>\nПример использования: /kp6 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp6.zip", "kp6", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp6.zip", "kp6")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp7' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp7 <color> <alpha>\nПример использования: /kp7 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp7.zip", "kp7", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp7.zip", "kp7")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp8' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp8 <color> <alpha>\nПример использования: /kp8 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp8.zip", "kp8", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp8.zip", "kp8")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/kp9' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /kp9 <color> <alpha>\nПример использования: /kp9 #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp9.zip", "kp9", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/kp9.zip", "kp9")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши кнопки готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/carmenu' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /carmenu <color> <alpha>\nПример использования: /carmenu #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/carmenu.zip", "carmenu", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/carmenu.zip", "carmenu")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваше меню машины готово!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/speedometer' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /speedometer <color> <alpha>\nПример использования: /speedometer #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/speedometer.zip", "speedometer", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/speedometer.zip", "speedometer")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваш спидометр готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/road' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /road <color> <alpha>\nПример использования: /road #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/road.zip", "road", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/road.zip", "road")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Вари дороги готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/casino' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /casino <color> <alpha>\nПример использования: /casino #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/casino.zip", "casino", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/casino.zip", "casino")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваш худ казино готов!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if '/pickup' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            hex_color = j[1]
        except:
            await message.answer("❔ Пример использования: /pickup <color> <alpha>\nПример использования: /pickup #FF0000 0.4\nЦвет должен быть в HEX(например, #RRGGBB)! P.S. альфа не обязательна")
            return
        try:
            alpha = float(message.text.split()[2])
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/pickup.zip", "pickup", alpha)
        except:
            work_dir, output_zip_path = await color_optimized(hex_color, "zip/pickup.zip", "pickup")
        f = FSInputFile(str(output_zip_path))
        await y.delete()
        await message.answer_document(f, caption='<b>⚡️Ваши пикапы готовы!</b>', parse_mode='HTML')
        shutil.rmtree(work_dir)
    if "/edit" in message.text:
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(text="Открыть phohtoshop",web_app=types.WebAppInfo(url="https://pixlr.com/ru/express/")))
        await message.answer("<b>⚡️Держи редактор:</b>", reply_markup=builder.as_markup(), parse_mode='HTML')
    if "/timecyc" in message.text and len(message.text.split()) >= 5:
        y = await message.answer("Обрабатываю...")
        output_file_path = await timecyc(j)
        await y.delete()
        f = FSInputFile(output_file_path)
        await bot.send_document(message.chat.id, f, caption='<b>⚡️TimeCycle готов!</b>', parse_mode='HTML')
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
    elif "/timecyc" in message.text and len(message.text.split()) < 5:
        await message.answer("❔ Пример использования: /timecyc SkyBottomRGB SkyTopRGB SunCoreRGB CloudRGB\nЗначение цветов /timecyc #НизНеба #ВерхНеба #Облака #Солнце\nВсе цвета должны быть в HEX(например, #RRGGBB)!")
    elif "/weapon" in message.text and len(message.text.split()) >= 3:
        y = await message.answer("Обрабатываю...")
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        n = rand_string
        try:
            PT = int(j[1])
            RAZB = int(j[2])
        except (ValueError, IndexError):
            await y.delete()
            await message.answer("Неверный формат данных. Используйте: /pistol <PT> <RAZB>")
        with open("weapon.isx", "r") as file:
            dg = file.read()
            dg = dg.replace("ПТ", str(PT))
            dg = dg.replace("RAZB", str(RAZB))
            output_file_name = f"{n}_weapon.dat"
        with open(output_file_name, "w") as file:
            file.write(dg)
        await y.delete()
        await message.answer_document(FSInputFile(output_file_name, filename=output_file_name),caption=f"<b>Держи weapon⚡</b>\nКоличество патрон в магазине: {PT}\nРазброс патрон: {RAZB}", parse_mode='HTML')
        os.remove(output_file_name)
    elif "/weapon" in message.text and len(message.text.split()) < 3:
        await message.answer("❔ Неверный формат данных. Используйте: /pistol <PT> <RAZB>\n\nПример использования: /weapon 9 50")
    elif "/colorcyc" in message.text and len(message.text.split()) >= 2:
        y = await message.answer("Обрабатываю...")
        if is_float(j[1]):
            black = j[1]
            grn1 = await colorcyc(black, black, black)
        else:
            hex_color = j[1]
            r1, g1, b1 = ImageColor.getrgb(hex_color)
            r, g, b = (str(round(c / 100, 3)) for c in [r1, g1, b1])
            grn1 = await colorcyc(r, g, b)
        user_id = message.from_user.id
        document = FSInputFile(grn1)
        await y.delete()
        await bot.send_document(user_id,document,caption='⚡️<b>Ваш colorcycle готов!</b>',parse_mode='HTML')
        os.remove(grn1)
    elif "/colorcyc" in message.text and len(message.text.split()) < 2:
        await message.answer("❔ Неверный формат данных. Используйте: /colorcyc <color>\n\nПример использования: /colorcyc 1.2 или /colorcyc #FF0000")
    elif "/checkcolor" in message.text and len(message.text.split()) >= 2:
        y = await message.answer("Обрабатываю...")
        hex_color = j[1]
        image_path = await kvadratik(hex_color)
        document = FSInputFile(image_path)
        user_id = message.from_user.id
        await y.delete()
        await bot.send_photo(user_id, document, caption=f'🎨<b>Палитра цвета - {hex_color} </b>', parse_mode='HTML')
        os.remove(image_path)
    elif "/checkcolor" in message.text and len(message.text.split()) < 2:
        await message.answer("❔ Неверный формат данных. Используйте: /checkcolor <color>\n\nПример использования: /checkcolor #FF0000")
    elif "/weather" in message.text and len(message.text.split()) >= 2:
        y = await message.answer("Обрабатываю...")
        id = j[1]
        with open('weather.json', 'r') as f:
            template_data = f.read()
        final_data = template_data.replace("ID", id)
        name = "mapzones.json"
        with open(name, 'w') as f:
            f.write(final_data)
        document = FSInputFile(name)
        user_id = message.from_user.id
        await y.delete()
        await bot.send_document(user_id, document, caption='⚡️<b>Держите погоду!</b>', parse_mode='HTML')
        os.remove(name)
    elif "/weather" in message.text and len(message.text.split()) < 2:
        await message.answer("❔ Неверный формат данных. Используйте: /weather <ID>\n\nПример использования: /weather 2\n\n⭐️ Список айди погоды:\n2 = дождь\n8 = гроза\n9 = густой туман и пасмурно\n10 = ясное небо\n11 = дикое пекло\n12 - 15 = смуглая и неприятная погода\n16 = тусклая и дождливая\n17 - 18 = жара\n19 = песчаная буря\n20 = туманная погода\n21 = ночь с пурпурным небом\n22 = ночь с зеленоватым небом\n23 - 26 = изменения бледного апельсина\n27 - 29 = изменения свежий синие\n30 - 32 = изменения темного, неясного, чирка\n33 = вечер в коричневатых оттенках\n34 = погода с синими/пурпурными оттенками\n35 = тусклая и унылая погода в коричневых тонах\n36 - 38 = яркая и туманная погода в тонах апельсина\n39 = очень яркая погода\n40 - 42 = неясная погода в пурпурных/синих цветах\n43 = тёмные и едкие облака\n44 = чёрно-белое небо\n45 = пурпурное небо")
    elif '/particle' in message.text and len(message.text.split()) >= 2:
        try:
            user = message.from_user.id
            y = await message.answer("Обрабатываю...")
            j = message.text.split()
            if len(j) < 3:
                await bot.send_message(user, "Неверный формат команды. Используйте: /particle <цвет> <размер>")
                return
            rgb = ImageColor.getrgb(j[1])
            if len(j) < 2:
                await bot.send_message(user, "Неверный формат команды. Используйте: /particle <цвет> <размер> <время> <гравитация> <разброс>")
                return
            r, g, b = map(str, rgb)
            q = "some_unique_q_value"
            r_value = "some_unique_r_value"
            work_dir = Path(f'work/work_BLOOD/{q}')
            work_dir.mkdir(parents=True, exist_ok=True)
            grn1_path = work_dir / f'{r_value}_particle.cfg'
            with open('particleCH.cfg', 'r') as infile:
                t = infile.read()
            t = t.replace("r22", r) \
                .replace("g22", g) \
                .replace("b22", b)
            if len(j) > 2:
                raz = j[2]
                time = j[3]
                grav = j[4]
                rzbros = j[5]
                t = t.replace("Q11", raz)\
                    .replace("U11", grav)\
                    .replace("R11", rzbros)\
                    .replace("T11", time)
            with open(grn1_path, 'w') as outfile:
                outfile.write(t)
            document = FSInputFile(grn1_path)
            await y.delete()
            await bot.send_document(user, document, caption='⚡️ Ваш particle.cfg готов!')
        except (ValueError, IndexError) as e:
            await bot.send_message(user, f"Ошибка при обработке параметров цвета или команды: {e}")
        except Exception as e:
            await bot.send_message(user, f"Произошла непредвиденная ошибка: {e}")
        finally:
            if 'work_dir' in locals() and work_dir.exists():
                shutil.rmtree(work_dir)
    elif '/search' in message.text.split():
        y = await message.answer("Обрабатываю...")
        try:
            args = j[1]
        except:
            await message.answer("❔ Пример использования: /skin <ID or NAME> \nПример использования: /skin 11")
            return
        query = j[1].strip()
        results = search_in_skins(query)
        if results is None:
            await message.answer("Ошибка при чтении файла skins.txt")
        elif not results:
            await message.answer(f"Нет информации о - {query} ID/NAME")
        else:
            id_xyina, name_xyina = results[0]
            attached_files = await file(id_xyina, name_xyina, message)
            response = []
            if attached_files:
                response.extend(attached_files)
                response.append("")
            response.append(f"ID - {id_xyina}")
            response.append(f"NAME - {name_xyina}")

            full_response = "\n".join(response)
            if not attached_files:
                await message.answer(full_response)
    elif '/skin' in message.text.split():
        try:
            user_id = message.from_user.id
            document = FSInputFile(f"skin/{message.text.split()[1]}.dff")
            document2 = FSInputFile(f"texture/texture_{message.text.split()[1]}.zip")
            await bot.send_document(user_id, document, caption='⚡️<b>Держите cкин!</b>', parse_mode='HTML')
            await bot.send_document(user_id, document2, caption='⚡️<b>Держите текстуры!</b>', parse_mode='HTML')
        except:
            await message.answer("Такого названия нет")
    elif '/car' in message.text.split():
        try:
            user_id = message.from_user.id
            document = FSInputFile(f"car/{message.text.split()[1]}.mod")
            await bot.send_document(user_id, document, caption='⚡️<b>Держите машину!</b>', parse_mode='HTML')
        except:
            await message.answer("Такого названия нет")
    elif "/help" in message.text:
        await message.answer("""<b>Привет👋 Вот возможности бота:</b>
        
<b>📌 Основные команды:</b>
/start — начать работу с ботом
/mysub — показать информацию о подписке
/edit - Запуск фотошопа
/help - Помощь

<b>🎨 Перекраска изображений:</b>
/color - Покраска Изображений
/recolor - Перекраска цвета
/hud1 - Перекраска белого hud
/hud2 - Перекраска полупрозрачного hud
/hud3 - Перекраска оригинального hud
/hud4 - Перекраска нового hud
/hp1 - Перекраска оригинального hud
/hp2 - Перекраска белого hud
/hud3 - Перекраска нового hud
/blood - Перекраска кастом крови
/tree - Перекраска оригинальной листвы
/vctree - Перекраска листвы стиля GTA Vice City
/kp1 - Перекраска белых с обводкой
/kp2 - Перекраска кнопок с блуд раша
/kp3 - Перекраска прозрачные черных кнопок
/kp4 - Перекраска серых кнопок
/kp5 - Перекраска gta5 кнопок
/kp6 - Перекраска smart кнопок
/kp7 - Перекраска vine кнопок
/kp8 - Перекраска коричневых кнопок
/kp9 - Перекраска оригинальных кнопок
/carmenu - Перекраска меню в машине
/speedometer - Перекраска спидометра машины
/road - Перекраска дорог
/casino - Перекраска Казино
/pickup - Перекраска пикапов
/filters
└ red - усиление красного канала
└ green - усиление зеленого канала
└ blue - усиление синего канала
└ grayscale - применение эффекта чёрно - белой палитры
└ negate - создание эффекта негатива
└ sepia - добавление теплого сепийного тона
└ solarize - эффект передержки изображения

<b>📂 Создание файлов:</b>
/weapon - Создание weapon.dat
/timecyc - сгенерировать оптимизированный TimeCycle
/colorcyc - сгенерировать ColorCycle
/particle - создание кастом крови
/genrl - создание кастом звуков бр
/bpc - шифровка bpc

<b>🧰 Копирование:</b>
/logo - Копирование Логотипов
/bild - Копирование Билбордов
/tree - Копирование Листвы

<b>✂️ Нарезка:</b>
/hudcut - Нарезка hud
/map - Нарезка map
/remap - Восстановить map
/rehud - Восстановить hud

<b>🌐 Дополнительно :</b>
/checkcolor - Палитра цвета
/aim - Конвертация Прицела
/weather - Создание Погоды
/compress - Сжатие веса
/search - Получить название из ID и наоборот(cкин)

<b>📁 Автоматически:</b>
<i><b>файл.btx/.png/.jpg/.zip</b></i> - обработка BTX,PNG,JPG
<i><b>файл.txd</b></i> - расшифровка 
TXD
<i><b>файл.bpc</b></i> - расшифровка 
bpc
<i><b>файл.ifp </b></i>- расшифровка анимаций
<i><b>файл.cls</b></i> - расшифровка коллизий
<i><b>файл.mod</b></i> - расшифровка моделей
<i><b>timecyc.dat</b></i>- конвертация Samp неба в Black Russia
<i><b>timecyc.json</b></i> - узнать цвета из Timecyc""", parse_mode='HTML')

    elif "/sub" in message.text and len(message.text.split()) >= 3:
        sender_id = message.from_user.id
        admin_status_row = execute_sql_query("SELECT admin FROM users WHERE chat_id=?", (sender_id,), fetchone=True)
        if admin_status_row and admin_status_row[0] == 'True':
            target_user_id = int(j[1])
            target_user_row = execute_sql_query("SELECT username FROM users WHERE chat_id=?", (target_user_id,),
                                                fetchone=True)

            if target_user_row:
                target_username = target_user_row[0]
                action = j[2]
                if len(j) == 4 and action == 'True':
                    expiry_date_str = j[3]
                    try:
                        datetime.datetime.strptime(expiry_date_str, "%d.%m.%Y")
                        execute_sql_query("UPDATE users SET sub='True', time=? WHERE chat_id=?",
                                          (expiry_date_str, target_user_id))
                        await message.answer(
                            f'Пользователю {target_username} успешно выдана подписка до {expiry_date_str}!')
                    except ValueError:
                        await message.answer("Неверный формат даты! Используйте %d.%m.%Y.")
                elif action == 'False':
                    execute_sql_query("UPDATE users SET sub='False', time=NULL WHERE chat_id=?", (target_user_id,))
                    await message.answer(f"У пользователя {target_username} успешно забрана подписка!")

                else:
                    await message.answer("Неверный формат команды или статуса подписки ('True'/'False')!")
            else:
                await message.answer(f"Пользователь с ID {target_user_id} не найден в базе данных.")
        else:
            await message.answer("У вас нет прав администратора для выполнения этой команды.")

    elif "/kotek" in message.text:
        await update(message.chat.id, message.from_user.username)  # Убеждаемся, что админ в БД
        sender_id = message.from_user.id

        admin_status_row = execute_sql_query("SELECT admin FROM users WHERE chat_id=?", (sender_id,), fetchone=True)

        if admin_status_row and admin_status_row[0] == 'True':
            # Получаем список всех chat_id из базы данных
            all_users = execute_sql_query("SELECT chat_id FROM users", fetchall=True)

            message_to_send = message.text.replace("/rass", "").strip()

            if message_to_send:
                for user_row in all_users:
                    user_id = user_row[0]
                    try:
                        # Асинхронная отправка сообщения
                        await bot.send_message(user_id, message_to_send)
                        # Можно добавить небольшую задержку, чтобы Telegram не забанил за спам
                        await asyncio.sleep(0.1)
                    except Exception as e:
                        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
                await message.answer(f"Рассылка завершена для всех пользователей.")
            else:
                await message.answer("Введите текст рассылки после команды /rass.")
        else:
            await message.answer("У вас нет прав администратора для выполнения этой команды.")

    elif "/send" in message.text:
        sender_id = message.from_user.id
        target_id_str = j[1]
        admin_status_row = execute_sql_query("SELECT admin FROM users WHERE chat_id=?", (sender_id,), fetchone=True)
        if admin_status_row and admin_status_row[0] == 'True':
            try:
                target_id = int(target_id_str)
                text_to_send = message.text.replace("/send", "").replace(target_id_str, "").strip()
                if text_to_send:
                    await bot.send_message(target_id, text_to_send)
                    await message.answer(f"Сообщение успешно отправлено пользователю {target_id}.")
                else:
                    await message.answer("Введите текст сообщения после ID получателя.")
            except ValueError:
                await message.answer("Неверный формат ID получателя.")
            except Exception as e:
                await message.answer(f"Ошибка при отправке сообщения: {e}")
        else:
            await message.answer("У вас нет прав администратора для выполнения этой команды.")


async def main() -> None:
    await setup_work_dirs()
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())


