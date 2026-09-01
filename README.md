# IMDb Movie Classification - MLOps Pipeline

Ovaj projekat predstavlja MLOps pajplajn za klasifikaciju IMDb filmova na osnovu njihovih karakteristika. Cilj projekta je automatizacija celog životnog ciklusa mašinskog učenja — od verzionisanja podataka i pokretanja lokalne infrastrukture, do CI/CD provere performansi modela prilikom svakog Pull Request-a.

## Tehnologije i Arhitektura

Model i Analiza: Python, Scikit-Learn (Random Forest), Pandas
Verzionisanje podataka: DVC (Data Version Control)
Skladištenje i Baza: MinIO (S3 kompatibilni Remote) i PostgreSQL (kontejnerizovani)
Kontejnerizacija: Docker i Docker Compose
CI/CD i CML: GitHub Actions i CML (Continuous Machine Learning) za automatsko poređenje metrika i Quality Gate

---

## Uputstvo za reprodukciju

Sledite ove korake da biste reprodukovali ceo tok od nule na novoj mašini:

### 1. Kloniranje repozitorijuma

git clone [https://github.com/lazarevic05/ml_projekat.git](https://github.com/lazarevic05/ml_projekat.git)
cd ml_projekat

### 2. Pokretanje infrastrukture (MinIO i PostgreSQL)

Infrastruktura za skladištenje podataka i bazu se pokreće u Docker kontejnerima:
docker-compose up -d

MinIO Console je dostupna na http://localhost:9001 (korisnički podaci su definisani u docker-compose.yml).

### 3. Podešavanje Python okruženja

Preporučuje se korišćenje virtuelnog okruženja:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 4. Povlačenje verzionisanih podataka sa DVC-a

Inicijalizujte DVC i povucite podatke sa lokalnog MinIO skladišta:
dvc pull

### 5. Pokretanje MLOps pajplajna

Za pokretanje celog procesa obrade podataka, treniranja i evaluacije pokrenite:
dvc repro
DVC će automatski prepoznati da li je došlo do promena u kodu ili params.yaml fajlu i po potrebi izvršiti korake u pajplajnu, generišući svež metrics.json.

---

## CI/CD i CML Workflow

Projekat koristi CML (Continuous Machine Learning) integrisan u GitHub Actions workflow (.github/workflows/cml.yaml).

Kako funkcioniše provera:

1. Kada se otvori Pull Request sa sporedne grane ka main grani, GitHub Actions automatski pokreće CML.
2. CML izvršava dvc metrics diff i poredi rezultate izmenjenog modela sa modelom koji se trenutno nalazi na main grani.
3. Generiše se automatski izveštaj u vidu komentara na PR-u sa tabelom razlika u metrici (Accuracy, Precision, Recall).
4. Model Quality Gate: U skriptu je ugrađen prag kvaliteta (Accuracy >= 0.65). Ako model ne zadovolji postavljeni prag, u komentar se upisuje upozorenje i sugerišu izmene pre spajanja sa main granom.