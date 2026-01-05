# Titanic Kafka-ML

A small demonstration project that trains a Random Forest model to predict Titanic passenger survival, serves predictions via Streamlit, and demonstrates streaming predictions using Kafka.

## Repository structure

- `app/streamlit_app.py`: Streamlit UI to input passenger features and get predictions.
- `data/raw/`: Raw CSVs (`train.csv`, `test.csv`).
- `data/processed/cleaned_titanic.csv`: Cleaned dataset used for training.
- `kafka/producer.py`: Reads `data/raw/test.csv`, performs minimal preprocessing, and streams passenger records to Kafka topic `titanic_topic`.
- `kafka/consumer.py`: Kafka consumer that loads the trained model and prints survival predictions for incoming messages.
- `model/train_model.py`: Trains a `RandomForestClassifier` on the cleaned data and saves `model/titanic_model.pkl`.
- `docker/`: Docker and docker-compose configuration for running Kafka and Zookeeper.

## How the project works (workflow)

1. Data preparation
   - The cleaned dataset used to train the model is expected at `data/processed/cleaned_titanic.csv`.
   - A notebook or script should produce this cleaned CSV from `data/raw/` (this repo includes `notebooks/01_data_cleaning.py`).

2. Train the model
   - Run `model/train_model.py` to train a Random Forest model and save it to `model/titanic_model.pkl`.

3. Stream predictions via Kafka (optional)
   - Start Kafka and Zookeeper (see Docker instructions) and run `kafka/producer.py` to stream passenger records from `data/raw/test.csv` to the Kafka topic `titanic_topic`.
   - Run `kafka/consumer.py` to consume messages and print model predictions in real time.

4. Use the Streamlit app (UI)
   - Run the Streamlit app `app/streamlit_app.py` to input passenger details and get a prediction using the saved model.

## Commands — Local (Python) setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate    # on Windows use: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Train the model:

```bash
python model/train_model.py
```

This will read `data/processed/cleaned_titanic.csv`, train a Random Forest model, print accuracy, and write `model/titanic_model.pkl`.

3. Run the Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

Open the URL printed by Streamlit (usually `http://localhost:8501`). The UI loads the saved model from `model/titanic_model.pkl` and predicts survival for the inputs.

4. Run Kafka producer & consumer (streaming demo)

- Start Kafka & Zookeeper using Docker Compose (see next section).
- In one terminal run the consumer to listen and predict:

```bash
python kafka/consumer.py
```

- In another terminal run the producer to stream test passengers:

```bash
python kafka/producer.py
```

The producer reads `data/raw/test.csv`, performs minimal preprocessing (fills `Age`/`Fare`, computes `FamilySize`, encodes `Sex`) and sends JSON messages to the `titanic_topic`. The consumer loads `model/titanic_model.pkl` and prints predictions for each message.

## Docker (Kafka) — quick start

From the `docker/` directory you can start Zookeeper and Kafka using the included `docker-compose.yml`:

```bash
cd docker
docker-compose up -d
```

This exposes Kafka on `localhost:9092` and Zookeeper on `localhost:2181` matching the producer/consumer configuration.

To stop and remove the services:

```bash
docker-compose down
```

Note: If you already run Kafka differently (Confluent, cloud), ensure `bootstrap_servers` in `kafka/producer.py` and `kafka/consumer.py` points to the correct broker.

## Code explanation (key files)

- `model/train_model.py`:
  - Loads `data/processed/cleaned_titanic.csv`.
  - Uses features `['Pclass','Sex','Age','Fare','FamilySize']` to train a `RandomForestClassifier`.
  - Splits data with `train_test_split(test_size=0.2, random_state=42)`.
  - Trains and evaluates accuracy, then saves the model to `model/titanic_model.pkl`.

- `kafka/producer.py`:
  - Loads `data/raw/test.csv` (which lacks the `Survived` column), performs small preprocessing (fills missing `Age`/`Fare`, computes `FamilySize`, maps `Sex` to 0/1), and streams each passenger as JSON to Kafka topic `titanic_topic`.

- `kafka/consumer.py`:
  - Loads `model/titanic_model.pkl` and starts a Kafka consumer subscribed to `titanic_topic`.
  - For each incoming message it constructs a DataFrame with the same features used for training and calls `model.predict()` to print whether the passenger would be predicted to survive.

- `app/streamlit_app.py`:
  - Provides a simple UI to enter passenger features and requests a prediction from the saved model.
  - Uses `@st.cache_resource` to cache loading of `model/titanic_model.pkl`.

## Important notes and assumptions

- The Streamlit app and Kafka consumer expect `model/titanic_model.pkl` to exist. Run `model/train_model.py` first.
- The producer and consumer use `localhost:9092` — ensure Docker Compose or another Kafka instance exposes that address.
- Data cleaning is assumed to be done beforehand; the cleaned file must contain `Survived` for training and the features the model expects.

## Troubleshooting

- If Kafka connection fails, confirm Docker containers are up (`docker ps`) and ports are not blocked.
- If the model file is not found, ensure `model/train_model.py` completed successfully and created `model/titanic_model.pkl`.

## Next steps (suggested)

- Add a small script to run preprocessing end-to-end and generate `data/processed/cleaned_titanic.csv` automatically.
- Add logging and error handling to `kafka/consumer.py` for production readiness.

---

If you'd like, I can also:
- run the training locally and verify the model file is produced,
- add a small `Makefile` or `run.sh` to simplify commands, or
- create a minimal README badge and usage examples for Docker Hub deployment.
