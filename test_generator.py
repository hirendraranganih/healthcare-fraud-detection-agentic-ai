from src.data_generator import generate_claims

df = generate_claims()

print(df.head())

print(df.shape)