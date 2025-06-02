from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Notes(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "done": self.done,
        }


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    new_note = Notes(
        title=data.get("title"),
        content=data.get("content", ""),
        done=data.get("done", False),
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = Notes.query.all()
    return jsonify([note.to_dict() for note in notes]), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Notes.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note supprimée"}), 200


# Initialisation de la base de données
@app.before_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
