import sqlite3 as sql

def crteDB():
    conec= sql.connect("zonacita.db")
    conec.commit()
    conec.close()

def borra_tabla(tab):
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    inst=f"DROP TABLE {tab}"
    db.execute(inst)  
    conec.commit()
    conec.close()

def crteTZonas():
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE zonas (
        id_zona integer,
        id_parr_zona integer,
        descrip_zona text,
        respo_zona text,
        telef_zona text,
        direc_zona text,
        primary key(id_zona)
        )"""
    )
    conec.commit()
    conec.close()

def crteTUsers():
    # sqlite crea en las tablas un campo rowid que es autoincemental
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE users (
        ci_users integer,
        nomb_users text,
        apell_users text,
        telef_users text,
        id_teleg_users integer,
        zona_users integer,
        tipo_users integer,
        primary key(ci_users)
        )"""
    )
    conec.commit()
    conec.close()   

def crteTtrans():
    # sqlite crea en las tablas un campo rowid que es autoincemental
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE IF NOT EXISTS transaccion (
        id_trans integer,
        ci_users integer,
        nomb_users text,
        apell_users text,
        id_teleg_users integer,
        zona_users integer,
        tipo_trans integer,
        fech_trans datetime,
        edo_trans integer,
        primary key(id_trans)
        )"""
    )
    conec.commit()
    conec.close() 

def crteTtransTy():
    # sqlite crea en las tablas un campo rowid que es autoincemental
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE IF NOT EXISTS transTipo (
        id_transti integer,
        descr_transti text,
        primary key(id_transti)
        )"""
    )
    conec.commit()
    conec.close()

def crteTusers():
    # sqlite crea en las tablas un campo rowid que es autoincemental
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE IF NOT EXISTS users (
        id_telegram integer,
        nomb_user text,
        apell_user text,
        niv_user integer,
        primary key(id_telegram)
        )"""
    )
    conec.commit()
    conec.close()    

def crteTmunicipio():
    # sqlite crea en las tablas un campo rowid que es autoincemental
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE IF NOT EXISTS municipio (
        id_muni integer,
        desc_muni text,
        primary key(id_muni)
        )"""
    )
    conec.commit()
    conec.close()   

def crteTparroquia():
    # sqlite crea en las tablas un campo rowid que es autoincemental
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE IF NOT EXISTS parroquia (
        id_parro integer,
        desc_parro text,
        id_muni_parro integer,
        primary key(id_parro)
        )"""
    )
    conec.commit()
    conec.close() 

def crteTCita():
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    db.execute(
        """CREATE TABLE citas (
        id_cita integer,
        ci_user_cita integer,
        fech_peti_cita datetime,
        fech_dia_cita datetime,
        id_trans_cita integer,
        primary key(id_cita)
        )"""
    )
    conec.commit()
    conec.close()

def bor_regis(tabla, campo, wheres):
   print(campo)
   pass

def upd_tabla(tabla, campo, wheres):
   pass


def ins_tabla(tabla, c1, c2,c3,c4,c5,c6,c7,c8,c9,oper):
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    if oper == "campos":
        if tabla == 'citas':
            instru = f"INSERT INTO citas VALUES (NULL,'{c2}','{c3}','{c4}','{c5}')"
        elif tabla == 'transTipo':
            instru = f"INSERT INTO transTipo VALUES ('NULL','{c2}')"
        elif tabla == 'transaccion':
            instru = f"INSERT INTO transaccion VALUES (NULL,{c2},'{c3}','{c4}',{c5},{c6},{c7},'{c8}',{c9})"
        elif tabla == 'users':
            instru = f"INSERT INTO users VALUES ('NULL','{c2}','{c3}','{c4}','{c5}','{c6}','{c7}')"
        else:
            instru = f"INSERT INTO {tabla} VALUES ('NULL')"
    else:
        instru = f"INSERT INTO {tabla} VALUES ({c1})"
      
    db.execute(instru)
    rowid = f"SELECT last_insert_rowid() FROM {tabla} LIMIT 1"
    db.execute(rowid)
    dat=db.fetchall()
    conec.commit()
    conec.close()
    
    return dat 

def lee_tabla(tabla, wheres, where2, tipo):
    conec= sql.connect("zonacita.db")
    db = conec.cursor()
    if tipo == 'b':
        instru = f"SELECT * FROM {tabla} WHERE {wheres}"
    elif tipo == 'n':
        instru = f"SELECT * FROM {tabla} WHERE {wheres} AND {where2}"
    else:
        instru = f"SELECT * FROM {tabla} WHERE 1"
    db.execute(instru)
    dat = db.fetchall()
    conec.commit()
    conec.close()
    return dat
