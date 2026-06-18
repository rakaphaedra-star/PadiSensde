"""
db_utils.py — PadiSense Database Utility (Supabase / PostgreSQL version)
Handles semua koneksi dan query ke database PostgreSQL (Supabase)
"""

import psycopg2
import psycopg2.extras
from psycopg2 import Error
import hashlib
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

try:
    import streamlit as st
    _HAS_STREAMLIT = True
except ImportError:
    _HAS_STREAMLIT = False

# ─── Konfigurasi Database ─────────────────────────────────────────────────────
def _get_db_config() -> Dict[str, Any]:
    """Ambil config dari Streamlit secrets (cloud) atau fallback ke default (lokal)."""
    if _HAS_STREAMLIT:
        try:
            return {
                "host":     st.secrets["supabase"]["host"],
                "port":     int(st.secrets["supabase"]["port"]),
                "dbname":   st.secrets["supabase"]["database"],
                "user":     st.secrets["supabase"]["user"],
                "password": st.secrets["supabase"]["password"],
            }
        except Exception:
            pass
    # Fallback (isi manual kalau mau test lokal tanpa secrets.toml)
    return {
        "host":     "aws-1-ap-south-1.pooler.supabase.com",
        "port":     5432,
        "dbname":   "postgres",
        "user":     "postgres.kstakjpvpefacagvcwwz",
        "password": "",  # isi password Supabase kamu di sini untuk testing lokal
    }

DB_CONFIG = _get_db_config()

# ─── Helper: Hash Password ────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ─── Koneksi ─────────────────────────────────────────────────────────────────
def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            connect_timeout=10,
        )
        return conn
    except Error as e:
        print(f"[DB ERROR] Gagal koneksi: {e}")
        return None

def test_connection() -> bool:
    conn = get_connection()
    if conn:
        conn.close()
        return True
    return False

# ─── Setup: Buat Tabel ───────────────────────────────────────────────────────
def setup_tables():
    """Tabel sudah dibuat manual via Supabase SQL Editor.
    Fungsi ini tetap ada agar pemanggilan dari login.py/register.py tidak error,
    tapi tidak melakukan apa-apa karena schema sudah final di Supabase."""
    conn = get_connection()
    if not conn:
        return False
    try:
        conn.close()
        return True
    except Error:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# ─── USER FUNCTIONS ───────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

def register_user(full_name: str, email: str, phone: str, password: str,
                  avatar_emoji: str = "👨‍🌾") -> Dict[str, Any]:
    conn = get_connection()
    if not conn:
        return {"success": False, "user_id": None, "message": "Database tidak bisa diakses."}
    try:
        cursor = conn.cursor()
        pw_hash = hash_password(password)
        cursor.execute(
            """INSERT INTO users (full_name, email, phone, password_hash, avatar_emoji)
               VALUES (%s, %s, %s, %s, %s) RETURNING id""",
            (full_name, email, phone, pw_hash, avatar_emoji)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "user_id": user_id, "message": "Registrasi berhasil!"}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        conn.close()
        return {"success": False, "user_id": None, "message": "Email sudah terdaftar!"}
    except Error as e:
        conn.rollback()
        conn.close()
        return {"success": False, "user_id": None, "message": str(e)}


def login_user(email: str, password: str) -> Dict[str, Any]:
    conn = get_connection()
    if not conn:
        return {"success": False, "user": None, "message": "Database tidak bisa diakses."}
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        pw_hash = hash_password(password)
        cursor.execute(
            """SELECT id, full_name, email, phone, avatar_emoji, created_at
               FROM users
               WHERE email = %s AND password_hash = %s AND is_active = 1""",
            (email, pw_hash)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return {"success": True, "user": dict(user), "message": "Login berhasil!"}
        else:
            return {"success": False, "user": None, "message": "Email atau password salah."}
    except Error as e:
        conn.close()
        return {"success": False, "user": None, "message": str(e)}


def update_password(user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
    conn = get_connection()
    if not conn:
        return {"success": False, "message": "Database tidak bisa diakses."}
    try:
        cursor = conn.cursor()
        old_hash = hash_password(old_password)
        cursor.execute(
            "SELECT id FROM users WHERE id = %s AND password_hash = %s",
            (user_id, old_hash)
        )
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {"success": False, "message": "Password saat ini tidak cocok."}
        new_hash = hash_password(new_password)
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (new_hash, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Password berhasil diperbarui!"}
    except Error as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": str(e)}


def update_avatar(user_id: int, avatar_emoji: str) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET avatar_emoji = %s WHERE id = %s",
            (avatar_emoji, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error:
        conn.rollback()
        conn.close()
        return False


def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT id, full_name, email, phone, avatar_emoji, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(user) if user else None
    except Error:
        conn.close()
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# ─── LOGIN HISTORY FUNCTIONS ──────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

def log_login(user_id: int, user_email: str, user_name: str,
              action: str = "login") -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO login_history (user_id, user_email, user_name, action)
               VALUES (%s, %s, %s, %s)""",
            (user_id, user_email, user_name, action)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"[DB ERROR] log_login: {e}")
        conn.rollback()
        conn.close()
        return False


def get_login_history(user_id: int, limit: int = 20) -> List[Dict]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """SELECT action, login_at FROM login_history
               WHERE user_id = %s ORDER BY login_at DESC LIMIT %s""",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]
    except Error:
        conn.close()
        return []


def get_all_login_history(limit: int = 50) -> List[Dict]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """SELECT lh.action, lh.login_at, lh.user_email, lh.user_name, u.full_name
               FROM login_history lh
               LEFT JOIN users u ON lh.user_id = u.id
               ORDER BY lh.login_at DESC LIMIT %s""",
            (limit,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]
    except Error:
        conn.close()
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# ─── SCAN HISTORY FUNCTIONS ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

def save_scan(user_id: int, user_name: str, disease_key: str,
              disease_label: str, confidence: float, status: str) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO scan_history
               (user_id, user_name, disease_key, disease_label, confidence, status)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, user_name, disease_key, disease_label,
             round(float(confidence), 2), status)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"[DB ERROR] save_scan: {e}")
        conn.rollback()
        conn.close()
        return False


def get_scan_history(user_id: int, limit: int = 100,
                     filter_status: str = "Semua",
                     filter_disease: str = "Semua") -> List[Dict]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        where  = ["user_id = %s"]
        params = [user_id]
        if filter_status != "Semua":
            where.append("status = %s")
            params.append(filter_status)
        if filter_disease != "Semua":
            where.append("disease_label = %s")
            params.append(filter_disease)
        params.append(limit)
        sql = f"""
            SELECT id, disease_key, disease_label, confidence, status, scanned_at
            FROM scan_history
            WHERE {' AND '.join(where)}
            ORDER BY scanned_at DESC
            LIMIT %s
        """
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]
    except Error as e:
        print(f"[DB ERROR] get_scan_history: {e}")
        conn.close()
        return []


def get_scan_stats(user_id: int) -> Dict[str, Any]:
    conn = get_connection()
    if not conn:
        return {"total": 0, "sakit": 0, "sehat": 0, "avg_conf": 0.0}
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """SELECT
                COUNT(*)                                                    AS total,
                SUM(CASE WHEN status='Terdeteksi' THEN 1 ELSE 0 END)        AS sakit,
                SUM(CASE WHEN status='Sehat' THEN 1 ELSE 0 END)             AS sehat,
                COALESCE(AVG(confidence), 0)                                AS avg_conf
               FROM scan_history WHERE user_id = %s""",
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "total":    int(row["total"]    or 0),
            "sakit":    int(row["sakit"]    or 0),
            "sehat":    int(row["sehat"]    or 0),
            "avg_conf": float(row["avg_conf"] or 0.0),
        }
    except Error:
        conn.close()
        return {"total": 0, "sakit": 0, "sehat": 0, "avg_conf": 0.0}


def delete_scan(scan_id: int, user_id: int) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM scan_history WHERE id = %s AND user_id = %s",
            (scan_id, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error:
        conn.rollback()
        conn.close()
        return False


def delete_all_scans(user_id: int) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM scan_history WHERE user_id = %s",
            (user_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error:
        conn.rollback()
        conn.close()
        return False


def get_unique_diseases(user_id: int) -> List[str]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT DISTINCT disease_label FROM scan_history
               WHERE user_id = %s ORDER BY disease_label""",
            (user_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [r[0] for r in rows]
    except Error:
        conn.close()
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# ─── CHAT HISTORY FUNCTIONS ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

def save_chat_message(user_id: int, role: str, content: str) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_id, role, content) VALUES (%s, %s, %s)",
            (user_id, role, content)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error:
        conn.rollback()
        conn.close()
        return False


def get_chat_history_db(user_id: int, limit: int = 50) -> List[Dict]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """SELECT role, content, created_at FROM chat_history
               WHERE user_id = %s ORDER BY created_at DESC LIMIT %s""",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return list(reversed([dict(r) for r in rows]))
    except Error:
        conn.close()
        return []


def clear_chat_history_db(user_id: int) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM chat_history WHERE user_id = %s",
            (user_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error:
        conn.rollback()
        conn.close()
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# ─── DISEASE INFO FUNCTIONS ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

def get_disease_info_db(disease_key: str) -> Optional[Dict]:
    """Tabel disease_info opsional — kalau belum dibuat di Supabase, fungsi ini
    akan mengembalikan None secara aman tanpa membuat aplikasi crash."""
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT * FROM disease_info WHERE disease_key = %s LIMIT 1",
            (disease_key,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(row) if row else None
    except Error:
        conn.close()
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# ─── GRAFIK / CHART QUERY FUNCTIONS ──────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

def get_weekly_trend(user_id: int, days: int = 28) -> List[Dict]:
    """
    Ambil jumlah scan Sehat vs Terdeteksi per hari selama N hari terakhir.
    Returns list of dicts: {tanggal, sehat, sakit, total}
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
            SELECT
                DATE(scanned_at)                                       AS tanggal,
                SUM(CASE WHEN status = 'Sehat' THEN 1 ELSE 0 END)       AS sehat,
                SUM(CASE WHEN status = 'Terdeteksi' THEN 1 ELSE 0 END)  AS sakit,
                COUNT(*)                                                AS total
            FROM scan_history
            WHERE user_id = %s
              AND scanned_at >= CURRENT_DATE - %s * INTERVAL '1 day'
            GROUP BY DATE(scanned_at)
            ORDER BY tanggal ASC
            """,
            (user_id, days)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]
    except Error as e:
        print(f"[DB ERROR] get_weekly_trend: {e}")
        conn.close()
        return []


def get_disease_distribution(user_id: int, days: int = 30) -> List[Dict]:
    """
    Distribusi jenis penyakit N hari terakhir (hanya status Terdeteksi).
    Returns list of dicts: {disease_label, jumlah}
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
            SELECT
                disease_label,
                COUNT(*) AS jumlah
            FROM scan_history
            WHERE user_id = %s
              AND status = 'Terdeteksi'
              AND scanned_at >= CURRENT_DATE - %s * INTERVAL '1 day'
            GROUP BY disease_label
            ORDER BY jumlah DESC
            """,
            (user_id, days)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]
    except Error as e:
        print(f"[DB ERROR] get_disease_distribution: {e}")
        conn.close()
        return []


def get_weekly_summary(user_id: int) -> Dict[str, Any]:
    """
    Ringkasan perbandingan minggu ini vs minggu lalu.
    Returns: {minggu_ini_sehat, minggu_ini_sakit, minggu_lalu_sehat, minggu_lalu_sakit}
    """
    conn = get_connection()
    if not conn:
        return {}
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
            SELECT
                SUM(CASE WHEN scanned_at >= CURRENT_DATE - INTERVAL '7 day'
                          AND status = 'Sehat' THEN 1 ELSE 0 END)      AS minggu_ini_sehat,
                SUM(CASE WHEN scanned_at >= CURRENT_DATE - INTERVAL '7 day'
                          AND status = 'Terdeteksi' THEN 1 ELSE 0 END) AS minggu_ini_sakit,
                SUM(CASE WHEN scanned_at >= CURRENT_DATE - INTERVAL '14 day'
                          AND scanned_at < CURRENT_DATE - INTERVAL '7 day'
                          AND status = 'Sehat' THEN 1 ELSE 0 END)      AS minggu_lalu_sehat,
                SUM(CASE WHEN scanned_at >= CURRENT_DATE - INTERVAL '14 day'
                          AND scanned_at < CURRENT_DATE - INTERVAL '7 day'
                          AND status = 'Terdeteksi' THEN 1 ELSE 0 END) AS minggu_lalu_sakit
            FROM scan_history
            WHERE user_id = %s
            """,
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "minggu_ini_sehat":  int(row["minggu_ini_sehat"]  or 0),
            "minggu_ini_sakit":  int(row["minggu_ini_sakit"]  or 0),
            "minggu_lalu_sehat": int(row["minggu_lalu_sehat"] or 0),
            "minggu_lalu_sakit": int(row["minggu_lalu_sakit"] or 0),
        }
    except Error as e:
        print(f"[DB ERROR] get_weekly_summary: {e}")
        conn.close()
        return {}
