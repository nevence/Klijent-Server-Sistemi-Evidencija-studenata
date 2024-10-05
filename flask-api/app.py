from functools import wraps
from flask import Flask, jsonify, request
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity

con = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    passwd='',
    database='evidencija_studenata'
)

mycursor = con.cursor(dictionary=True)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'tvoj_tajni_jwt_kljuc'
jwt = JWTManager(app)


def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"message": "Nemate dozvolu za pristup ovoj ruti."}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
# -----------------------------------------------> Login <-------------------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    forma = request.json
    upit = "SELECT * FROM korisnici WHERE email=%s"
    vrednost = (forma['email'],)
    mycursor.execute(upit, vrednost)
    korisnik = mycursor.fetchone()

    if korisnik and check_password_hash(korisnik['lozinka'], forma['lozinka']):
        access_token = create_access_token(
            identity=korisnik['email'],
            additional_claims={"role": korisnik['rola']}
        )
        return jsonify({"message": "Uspešno ste se prijavili.", "access_token": access_token, "rola": korisnik['rola']}), 200
    else:
        return jsonify({"message": "Neispravni podaci za prijavu."}), 401

# -----------------------------------------------> Studenti <-----------------------------------------------------

@app.route('/studenti', methods=['GET'])
@jwt_required()
def studenti():
    upit = "SELECT * FROM studenti"
    mycursor.execute(upit)
    studenti = mycursor.fetchall()
    return jsonify(studenti), 200


@app.route('/student/<int:id>', methods=['GET'])
@jwt_required()
def student(id):
    upit = "SELECT * FROM studenti WHERE id = %s"
    vrednost = (id,)
    mycursor.execute(upit, vrednost)
    student = mycursor.fetchone()

    upit_ocene = """
        SELECT *
        FROM predmeti
        JOIN ocene ON predmeti.id = ocene.predmet_id
        WHERE ocene.student_id = %s
    """
    mycursor.execute(upit_ocene, vrednost)
    ocene = mycursor.fetchall()

    upit_predmeti = "SELECT id, naziv FROM predmeti"
    mycursor.execute(upit_predmeti)
    predmeti = mycursor.fetchall()

    return jsonify({"student": student, "ocene": ocene, "predmeti": predmeti}), 200


@app.route('/student-novi', methods=['POST'])
@jwt_required()
def novi_student():
    data = request.json
    upit = """
        INSERT INTO studenti (broj_indeksa, ime, ime_roditelja, prezime, email, broj_telefona, godina_studija, datum_rodjenja, jmbg) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    vrednosti = (data['broj_indeksa'], data['ime'], data['ime_roditelja'], data['prezime'], data['email'], data['broj_telefona'], 
                 data['godina_studija'], data['datum_rodjenja'], data['jmbg'])
    mycursor.execute(upit, vrednosti)
    con.commit()
    return jsonify({"message": "Uspešno ste dodali novog studenta."}), 200


@app.route('/student-izmena/<int:id>', methods=['PUT'])
@jwt_required()
def student_izmena(id):
    data = request.json
    upit = """
        UPDATE studenti SET broj_indeksa=%s, ime=%s, ime_roditelja=%s, prezime=%s, email=%s, broj_telefona=%s, 
        godina_studija=%s, datum_rodjenja=%s, jmbg=%s WHERE id=%s
    """
    vrednosti = (data['broj_indeksa'], data['ime'], data['ime_roditelja'], data['prezime'], data['email'], data['broj_telefona'],
                 data['godina_studija'], data['datum_rodjenja'], data['jmbg'], id)
    mycursor.execute(upit, vrednosti)
    con.commit()
    return jsonify({"message": "Uspešno ste izmenili studenta."}), 200


@app.route('/student-brisanje/<int:id>', methods=['DELETE'])
@jwt_required()
def student_brisanje(id):
    mycursor.execute("DELETE FROM studenti WHERE id = %s", (id,))
    con.commit()
    return jsonify({"message": "Uspešno ste obrisali studenta."}), 200


# -----------------------------------------------> Korisnici <-----------------------------------------------------

@app.route('/korisnici', methods=['GET'])
@jwt_required()
@role_required(["administrator"])
def api_korisnici():
    mycursor.execute("SELECT * FROM korisnici")
    korisnici = mycursor.fetchall()
    return jsonify(korisnici), 200


@app.route('/korisnik-novi', methods=['POST'])
@jwt_required()
@role_required(["administrator"])
def api_novi_korisnik():
    forma = request.json
    upit = "INSERT INTO korisnici (ime, prezime, email, rola, lozinka) VALUES (%s, %s, %s, %s, %s)"
    hash_lozinka = generate_password_hash(forma['lozinka'])
    vrednosti = (forma['ime'], forma['prezime'], forma['email'], forma['rola'], hash_lozinka)
    mycursor.execute(upit, vrednosti)
    con.commit()
    return jsonify({"message": "Uspešno ste dodali novog korisnika."}), 200


@app.route('/korisnik/<int:id>', methods=['GET'])
@jwt_required()
@role_required(["administrator"])
def api_korisnik(id):
    mycursor.execute("SELECT ime, prezime, email, rola FROM korisnici WHERE id=%s", (id,))
    korisnik = mycursor.fetchone()

    if korisnik:
        return jsonify(korisnik), 200
    else:
        return jsonify({"error": "Korisnik nije pronađen"}), 404


@app.route('/korisnik-izmena/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(["administrator"])
def api_korisnik_izmena(id):
    forma = request.json
    upit = """
        UPDATE korisnici SET ime=%s, prezime=%s, email=%s, rola=%s, lozinka=%s WHERE id=%s
    """
    lozinka = generate_password_hash(forma['lozinka'])
    vrednosti = (forma['ime'], forma['prezime'], forma['email'], forma['rola'], lozinka, id)
    mycursor.execute(upit, vrednosti)
    con.commit()
    return jsonify({"message": "Uspešno ste izmenili korisnika."}), 200


@app.route('/korisnik-brisanje/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(["administrator"])
def api_korisnik_brisanje(id):
    mycursor.execute("DELETE FROM korisnici WHERE id = %s", (id,))
    con.commit()
    return jsonify({"message": "Uspešno ste obrisali korisnika."}), 200


# -----------------------------------------------> Predmeti <-----------------------------------------------------

@app.route('/predmeti', methods=['GET'])
@jwt_required()
@role_required(["administrator"])
def api_predmeti():
    mycursor.execute("SELECT * FROM predmeti")
    predmeti = mycursor.fetchall()
    return jsonify(predmeti), 200


@app.route('/predmet/<int:id>', methods=['GET'])
@jwt_required()
@role_required(["administrator"])
def api_predmet(id):
    mycursor.execute("SELECT * FROM predmeti WHERE id=%s", (id,))
    predmet = mycursor.fetchone()

    if predmet:
        return jsonify(predmet), 200
    else:
        return jsonify({"error": "Predmet nije pronađen"}), 404


@app.route('/predmet-izmena/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(["administrator"])
def api_predmet_izmena(id):
    forma = request.json
    upit = """
        UPDATE predmeti SET sifra=%s, naziv=%s, godina_studija=%s, espb=%s, obavezni_izborni=%s WHERE id=%s
    """
    vrednosti = (forma['sifra'], forma['naziv'], forma['godina_studija'], forma['espb'], forma['status'], id)
    mycursor.execute(upit, vrednosti)
    con.commit()
    return jsonify({"message": "Uspešno ste izmenili predmet."}), 200


@app.route('/predmet-brisanje/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(["administrator"])
def api_predmet_brisanje(id):
    mycursor.execute("DELETE FROM predmeti WHERE id = %s", (id,))
    con.commit()
    return jsonify({"message": "Uspešno ste obrisali predmet."}), 200


@app.route('/predmet-novi', methods=['POST'])
@jwt_required()
@role_required(["administrator"])
def api_novi_predmet():
    forma = request.json
    upit = """
        INSERT INTO predmeti (sifra, naziv, godina_studija, espb, obavezni_izborni) VALUES (%s, %s, %s, %s, %s)
    """
    vrednosti = (forma['sifra'], forma['naziv'], forma['godina_studija'], forma['espb'], forma['status'])
    mycursor.execute(upit, vrednosti)
    con.commit()
    return jsonify({"message": "Uspešno ste dodali novi predmet."}), 200

# -----------------------------------------------> Ocene <-----------------------------------------------------

@app.route("/ocene", methods=["POST"])
@jwt_required()
def api_nova_ocena():
    forma = request.json
    upit = "INSERT INTO ocene(student_id, predmet_id, ocena, datum) VALUES(%s, %s, %s, %s)"
    vrednosti = (forma['student_id'], forma['predmet_id'], forma['ocena'], forma['datum'])
    mycursor.execute(upit, vrednosti)
    con.commit()

    # Ažuriraj prosek i ESPB
    update_student_stats(forma['student_id'])
    return jsonify({"message": "Ocena uspešno dodata"}), 200


@app.route("/ocene/<int:student_id>/<int:ocena_id>", methods=["DELETE"])
@jwt_required()
def api_ocena_brisanje(student_id, ocena_id):
    upit = "DELETE FROM ocene WHERE id=%s"
    vrednost = (ocena_id,)
    mycursor.execute(upit, vrednost)
    con.commit()

    # Ažuriraj prosek i ESPB
    update_student_stats(student_id)
    return jsonify({"message": "Ocena uspešno obrisana"}), 200


def update_student_stats(student_id):
    # Ažuriraj prosek ocena
    upit = "SELECT AVG(ocena) AS prosek FROM ocene WHERE student_id=%s"
    mycursor.execute(upit, (student_id,))
    prosek_ocena = mycursor.fetchone()

    # Ažuriraj ukupno ESPB
    upit = "SELECT SUM(espb) AS espb FROM predmeti WHERE id IN (SELECT predmet_id FROM ocene WHERE student_id=%s)"
    mycursor.execute(upit, (student_id,))
    espb = mycursor.fetchone()

    # Update student
    upit = "UPDATE studenti SET espb=%s, prosek_ocena=%s WHERE id=%s"
    mycursor.execute(upit, (espb['espb'], prosek_ocena['prosek'], student_id))
    con.commit()


# Ruta za vraćanje liste proizvoda 
@app.route('/products', methods=['GET']) 
def get_products(): 
    products = [
        {"id": 1, "name": "Proizvod 1", "price": 100}, 
        {"id": 2, "name": "Proizvod 2", "price": 200}, 
        ]
	# jsonify funkcija koja konvertuje izlaz u JSON response objekat
    return jsonify(products) 


if __name__ == "__main__":
    app.run(debug=True)
