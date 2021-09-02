# -*- coding: utf-8 -*-
import threading

from flask import render_template, flash, redirect, request
from app import app
from app.database import device, db, conn
from app.forms import dev

lock = threading.Lock()

@app.route('/req', methods=['GET', 'POST'])
def req():  # if current_user.is_authenticated:
    #db.execute("select sectors.id_noms,sectors.object1, sectors.object2, sectors.object3,sectors.object4,sectors.object5 from sectors")
    #dv1 = db.fetchall()  # все девайсы
    #dvmy = dv1  # просто обЪявление dvmy
    #dvmypoisk = dv1
    #conn.commit()
    #form = dev()
    try:
        lock.acquire(True)
        db.execute("select sectors.id_noms,sectors.object1, sectors.object2, sectors.object3,sectors.object4,sectors.object5 from sectors")
        dv1 = db.fetchall()
        dvmy = dv1
        dvmypoisk = dv1
        conn.commit()
        form = dev()
    finally:
        lock.release()

    #дальше выборка
    if form.ppb.data == True:#search
        if form.object1.data == '':
            if form.object2.data == '':
                if form.object3.data == '':
                    if form.object4.data == '':
                        flash('poisk')
                        return render_template('req.html', title='devices', form=form, dv=dv1, dvmy=dvmy,
                                               dvmypoisk=dvmypoisk, )
                    else:
                      try:
                        lock.acquire(True)
                        db.execute(
                            "select sectors.id_noms,sectors.object1, sectors.object2, sectors.object3, sectors.object4,sectors.object5 from sectors where (sectors.object4 = ?);",
                            (form.object4.data,))
                        dvmypoisk = db.fetchall()
                      finally:
                        lock.release()
                      device.rr = form.object4.data  # для фильтрации!!!!!!!!!!!!!
                      if dvmypoisk == []:
                          flash(device.rr)
                          return render_template('req.html', title='devices', form=form, dv=dv1, dvmy=dvmy,
                                                   dvmypoisk=dvmypoisk, )
                else:
                  try:
                    lock.acquire(True)
                    db.execute(
                        "select sectors.id_noms,sectors.object1, sectors.object2, sectors.object3, sectors.object4,sectors.object5 from sectors where (sectors.object3 = ?);",
                        (form.object3.data,))
                    dvmypoisk = db.fetchall()
                  finally:
                    lock.release()
                  device.rr = form.object3.data  # для фильтрации!!!!!!!!!!!!!
                  if dvmypoisk == []:
                      flash(device.rr)
                      return render_template('req.html', title='devices', form=form, dv=dv1, dvmy=dvmy,
                                             dvmypoisk=dvmypoisk, )
            else:
              try:
                lock.acquire(True)
                db.execute(
                    "select sectors.id_noms,sectors.object1, sectors.object2, sectors.object3, sectors.object4,sectors.object5 from sectors where (sectors.object2 = ?);",
                    (form.object2.data,))
                dvmypoisk = db.fetchall()
              finally:
                lock.release()
              device.rr = form.object2.data  # для фильтрации!!!!!!!!!!!!!
              if dvmypoisk == []:
                  flash(device.rr)
                  return render_template('req.html', title='devices', form=form, dv=dv1, dvmy=dvmy,
                                         dvmypoisk=dvmypoisk, )
        else:
          try:
            lock.acquire(True)
            db.execute("select sectors.id_noms,sectors.object1, sectors.object2, sectors.object3, sectors.object4,sectors.object5 from sectors where (sectors.object1 = ?);",
                       (form.object1.data,))
            dvmypoisk = db.fetchall()
          finally:
            lock.release()
          device.rr = form.object1.data   #для фильтрации
          if dvmypoisk == []:
              flash(device.rr)
              return render_template('req.html', title='devices', form=form, dv=dv1, dvmy=dvmy,dvmypoisk=dvmypoisk,)
    if form.ppo.data == True:
        device.rr=None
        return redirect('/req')
    if form.addb.data == True:
        if form.object1.data == '':
            flash('Введите все поля')
            return redirect('/req')
        if form.object2.data == '':
            flash('Введите все поля')
            return redirect('/req')
        if form.object3.data == '':
            flash('Введите все поля')
            return redirect('/req')
        if form.object4.data == '':
            flash('Введите все поля')
            return redirect('/req')
        if form.object1.data != '':
            if form.object2.data != '':
                if form.object3.data != '':
                    if form.object4.data != '':
                                  try:
                                    lock.acquire(True)
                                    conn.execute('insert into sectors (object1,object2,object3,object4,object5) values (?,?,?,?,?);',
                                                 (form.object1.data, form.object2.data, form.object3.data, form.object4.data, form.object5.data))
                                    conn.commit()
                                  finally:
                                    lock.release()
                                  flash('device_db_dob!')
                                  return render_template('req.html', title='requests', form=form, dv=dv1, dvmy=dvmy,
                                                         dvmypoisk=dvmypoisk)
    dov1 = form.gr_del_num.data
    dov2 = form.gr_del_num1.data
    if request.method == 'POST':
        if request.form['del'] == 'del':
          flash(dov2)
          try:
            lock.acquire(True)
            conn.execute('delete from sectors where id_noms=? or id_noms=?',
                         (form.gr_del_num.data, form.gr_del_num1.data,) )
            conn.commit()
          finally:
            lock.release()
          flash('delete_ud!')
          return render_template('req.html', title='requests', form=form, dv=dv1, dvmy=dvmy,
                                 dvmypoisk=dvmypoisk)
    dv = dv1
    form.object1.data = device.rr # Для указания фильтрации в строке
    if device.rr!=None:
      try:
        lock.acquire(True)
        db.execute(
            'select sectors.id_noms,sectors.object1, sectors.object2, sectors.object3, sectors.object4,sectors.object5 from sectors where (sectors.object1 = ?);',
            (device.rr,))
        dv1=db.fetchall()
      finally:
        lock.release()
      return render_template('req.html', title='requests', form=form, dv=dv1, dvmy=dvmy,
                             dvmypoisk=dvmypoisk)
    return render_template('req.html', title='requests', form=form, dv=dv, dvmy=dvmy, dvmypoisk=dvmypoisk)

