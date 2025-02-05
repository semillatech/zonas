#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from datetime import date
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import csv 

from DBConnection import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

MUNI, PARRO, NAME, APELL, TRAM , END, ERR = range(7)

token = "8052827167:AAFephcqeszo-Uww4cgTOTeXQ-st0ZEQfMI"
user_name = "ZonaEDCbot"

def bsc_lst(matrix,posiciones):
    
    texto=""
    
    for row in matrix :
        if posiciones == 2:
            texto += str(row[0])+" "+row[1]+"\n"
        elif posiciones == 3:
            texto += str(row[0])+" "+row[1]+" "+row[2]+"\n"
        elif posiciones == 4:
            texto += str(row[0])+" "+row[1]+" "+row[2]+" "+row[3]+"\n"
        elif posiciones == 5:
            texto += str(row[0])+" "+row[1]+" "+row[2]+" "+row[3]+" "+row[4]+"\n"
        elif posiciones == 6:
            texto += str(str(row[0]))+" "+str(row[1])+" "+str(row[2])+" "+str(row[3])+"\n"
        elif posiciones == 9:
            texto += str(str(row[0]))+" "+str(row[1])+" "+str(row[2])+" "+str(row[3])+" "+str(row[4])+" "+str(row[5])+" "+str(row[6])+" "+str(row[7])+" "+str(row[8])+"\n"
        else:
            texto += str(row[0])+" "+row[1]+" "+row[2]+" "+row[3]+" "+row[4]+" "+row[5]+"\n"+"\n"

    return texto

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Bienvenid@ a ZonaEDCbot, puedes usar el menu en la barra del chat para\
    conocer los comandos disponibles o /registrar si eres usuario nuevo\n\n")
    #today = date.today()
    #now= datetime.now()
    #print(today)
    #print(now)
    #docu_pdf = open('requi1.pdf', 'rb')
    #await context.bot.send_document(update.message.chat_id, docu_pdf)

async def lee_stdo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """toma el no. transaccion consulta bd y obtiene estado del proceso"""
    cedula=10 #update.message.text
    matrix0 = lee_tabla('transaccion', f"ci_users = {cedula}","edo_trans != 9", "n")
    cedula_enc=0
    if len(matrix0) != 0: 
        cedula_enc=1
    
    if cedula_enc == 0:
        await update.message.reply_text(
            f"No existe ninguna transaccion con el numero de cedula {cedula} en proceso.\n\n")

        return
    else:
        fecha=matrix0[0][7]  #.strftime('%d-%m-%y')
        edo=matrix0[0][8]
        await update.message.reply_text(
        f"El proceso No. {matrix0[0][0]}, tramitado por la c.i. No.{matrix0[0][1]}, de fecha {fecha}, tiene un estado de: {edo}.")
        
        return
    

async def ins_camb_proce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # busco estado de solicitud en bd y asigno variables
    
    num_soli = "2025_02_00010"
    tipos = "1.- En Proceso...\n2.- Esperando cosignacion de documentos en su zona educativa\n3.- Espera Retiro documento finalizado tome cita\n4.-n....."
    estado =f"Los tipos de estado de proceso son: {tipos}"
    await update.message.reply_text(f"Hola! , este proceso esta aun en programacion")

async def ins_cita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # busco estado de solicitud en bd y asigno variables
    num_soli_ = "2025_02_00010"
    parro_ = "Zona Educativa ME"
    cita= datetime.today()
    estado_ =f"Aqui insertaran citas al terminar el proceso seleccionado cuando finalice para retirar documentos"
    await update.message.reply_text(f"Hola el proceso de cita aun esta en programacion...hoy {cita.strftime('%d-%m-%y')} ")

async def lee_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # busco estado de solicitud en bd y asigno variables
    matrix = lee_tabla('transaccion', "none","", "none")
    texto = bsc_lst(matrix,9)
    await update.message.reply_text(
        "lista de Procesos Almacenados Bd\n\n"
        f"{texto}\n\n")

#with open("parro.csv") as muni:
#leer = csv.reader(muni, delimiter=";" )
#for row in leer:
#   crgaTpquia(row[0], row[2], row[1])
    #ver=leer_muni()
    #print("a ver {0} es {1}".format(ver[0][0], ver[0][1]))
    #crteTparroquia()

# inicio conversa de registro
async def registro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    
    await update.message.reply_text(
        "Hola Bienvenido a ZonaEDCbot, para registrate necesitamos algunos datos "
        "envia el comando /cancelar para cancelar el proceso.\n\n"
        "Necesitamos el numero de tu cedula de identidad (solo numeros sin puntos ni letras)?"
    )

    return MUNI


async def muni(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """toma el municipio consulta bd y obtiene parroquias y pide la parroquia"""
    #reply_keyboard = [["Sucre", "Coche", "El Valle", "Caricuao"]]
    cedula=update.message.text
    matrix0 = lee_tabla('transaccion', f"ci_users = {cedula}","edo_trans != 9", "n")
    cedula_enc=0
    if len(matrix0) != 0: 
        cedula_enc=1
    context.user_data['ci_user'] = update.message.text
    matrix = lee_tabla('municipio', "none","", "none")
    texto = bsc_lst(matrix,2)
    if cedula_enc == 0:
        await update.message.reply_text(
            "lista de Municipios Distrito Capital\n\n"
            f"{texto}\n\n"
            f"la cedula de identidad enviada es: {context.user_data['ci_user']}, ahora necesitamos el municipio y la parroquia donde se encuantra el ultimo plantel donde cursaste tus estudios, envia el numero del municipio (ver lista arriba)?")

        return PARRO
    else:
        fecha=matrix0[0][7]  #.strftime('%d-%m-%y')
        await update.message.reply_text(
        f"El proceso No. {matrix0[0][0]}, tramitado por la c.i. No.{matrix0[0][1]}, de fecha {fecha}, aun no ha finalizado el proceso iniciado, debes esperar su culminacion para poder iniciar otro tramite.")
        context.user_data.clear()
        return ConversationHandler.END


async def parro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """guarda el municipio y pide la parroquia"""
    context.user_data['codmuni'] = update.message.text
    matrix = lee_tabla('municipio',f"id_muni = { context.user_data['codmuni']}" ,"", 'b')
    muni_enc=0
    if len(matrix) != 0: 
        muni_enc=1
    
    if muni_enc == 1:
        context.user_data['descmuni'] = matrix[0][1]
        textob = lee_tabla('parroquia', f"id_muni_parro = { context.user_data['codmuni']}","", 'b')
        texto = bsc_lst(textob, 2)
        # context.user_data.setdefault(('codimuni',munides[0]), ('descmuni',munides[1]))
        await update.message.reply_text(
            f"Lista de Parroquias en el municipio {context.user_data['descmuni']}\n\n"
            f"{texto}\n\n"
            f"Gracias!, ahora envia el numero de la parroquia (ver lista arriba)? ")

        return NAME

    else:
        await update.message.reply_text(
            f"Uste ha enviado un numero equivocado de municipio debe limitarse a la lista, pruebe /registrar nuevamente.")
        context.user_data.clear()
        
        return ConversationHandler.END


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """guarda parroquia y pregunto nombre"""
    context.user_data['codparr'] = update.message.text
    matrix = lee_tabla('parroquia', f"id_parro = { context.user_data['codparr']}","", 'b')
    parr_enc=0
    if len(matrix) != 0: 
        parr_enc=1

    if parr_enc == 1:
        context.user_data['descparr'] = matrix[0][1]
        await update.message.reply_text(
            f"que bien ; tu parroquia es { context.user_data['descparr']}, ahora envia tu primer nombre?"
        )

        return APELL
    else:
        await update.message.reply_text(
            f"Uste ha enviado un numero equivocado de parroquia debe limitarse a la lista, pruebe /registrar nuevamente.")
        context.user_data.clear()
        return ConversationHandler.END


async def apell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """guarda el nombre y pide el apellido"""
    context.user_data['nomb_user'] = update.message.text
    await update.message.reply_text(
        f"excelente, tu nombre es { context.user_data['nomb_user']}, faltan solo 2 pasos, cual es tu primer apellido?"
    )

    return TRAM

async def tram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """guarda el nombre y pide el apellido"""
    context.user_data['apell_user'] = update.message.text
    textob = lee_tabla('transTipo',"none","","none")
    texto = bsc_lst(textob,2)
    await update.message.reply_text(
        "Listas de Tipos de Transacciones:\n\n"
        f"{texto}\n\n"
        f"ok, tu apellido es { context.user_data['apell_user']}, por ultimo envia el numero del tipo de tramite a realizar (ver lista arriba)."
    )

    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    context.user_data['trans_user'] = update.message.text
    matrix = lee_tabla('transTipo',f"id_transti = { context.user_data['trans_user']}","", "b")
    trans_enc=0
    if len(matrix) != 0: 
        trans_enc=1

    if trans_enc == 1:
        ciuser =  context.user_data['ci_user']
        nombuser =  context.user_data['nomb_user']
        apelluser = context.user_data['apell_user']
        transuser = context.user_data['trans_user']
        codparr = context.user_data['codparr']
        context.user_data['desc_trans_user'] = matrix[0][1]
        desctransuser = context.user_data['desc_trans_user']
        today = date.today()
        idrow=ins_tabla('transaccion', 'NULL', ciuser, nombuser, apelluser, context._user_id,codparr,transuser, today,1,"campos")
        num_trans_= idrow[0][0]
        proc_="Exitoso"
        
        dat_=f"Liceo Nacional { context.user_data['descparr']} \nAv ppal { context.user_data['descparr']} entre\
            \nelevado entrada autopista \ntelegram: @ZonaEDC{ context.user_data['descparr']}"
        NU=str(context.user_data['trans_user'])
        docu_pdf = open(f'REQUISITOS{NU}.pdf', 'rb')
        
        complnom=nombuser+" "+apelluser
        await update.message.reply_text(
            f"Muchas gracias {complnom}, tu registro fue {proc_}, a continuacion sus datos registrados:\n\n"
            f"proceso no.: {num_trans_}\ntramite: {desctransuser}\n\n"
            f"Debes llevar los documentos solicitados en el archivo pdf que le suministramo, a la zona Educativa en el municipio { context.user_data['descmuni']} ubicado en:\n\n"
            f"{dat_}.\n\n"
            )
        await context.bot.send_document(update.message.chat_id, docu_pdf)
        logger.info("Gender of %s: %s", 'numero transaccion', num_trans_)
        context.user_data.clear()
        
        return ConversationHandler.END

    else:
        await update.message.reply_text(
            f"Uste ha enviado un numero equivocado de tramite debe limitarse a la lista, pruebe /registrar nuevamente.")
        context.user_data.clear()
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("Estimado(a) %s has cancelado el ciclo de preguntas.", user.first_name)
    await update.message.reply_text("Esperamos que intentes registrarte luego, hasta entonces.")
    context.user_data.clear()

    return ConversationHandler.END

async def err(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text("has ingresado un tipo de dato erroneo vuelve al comienzo /registrar ")
    context.user_data.clear()

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("registrar", registro)],
        states={
            MUNI: [MessageHandler(filters.TEXT, muni)],
            PARRO:  [MessageHandler(filters.TEXT & ~filters.COMMAND, parro)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            APELL: [MessageHandler(filters.TEXT & ~filters.COMMAND, apell)],
            TRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, tram)],
            END: [MessageHandler(filters.TEXT & ~filters.COMMAND, end)],
            ERR: [MessageHandler(filters.TEXT & ~filters.COMMAND, err)],
        },
        fallbacks=[CommandHandler("cancelar", cancel)],
    )
    
    application.add_handler(CommandHandler('start', ayuda))
    application.add_handler(CommandHandler('ayuda', ayuda))
    application.add_handler(CommandHandler('estado', lee_stdo))
    application.add_handler(CommandHandler('cita', ins_cita))
    application.add_handler(CommandHandler('listado', lee_lista))
    application.add_handler(CommandHandler('proceso', ins_camb_proce))
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()