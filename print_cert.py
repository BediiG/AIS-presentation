from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

with open("cert.pem", "rb") as f:
    cert_data = f.read()

cert = x509.load_pem_x509_certificate(cert_data, default_backend())

print("📄 ===== Certificate Info =====")
print(f"Subject: {cert.subject}")
print(f"Issuer: {cert.issuer}")
print(f"Valid From: {cert.not_valid_before_utc}")
print(f"Valid Until: {cert.not_valid_after_utc}")
print(f"Serial Number: {cert.serial_number}")
print(f"Public Key Type: {cert.public_key().__class__.__name__}")
print(f"Signature Algorithm: {cert.signature_algorithm_oid._name}")

print("\n🔓 Raw PEM Certificate:")
print(cert.public_bytes(encoding=serialization.Encoding.PEM).decode())
