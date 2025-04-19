from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# Generate key
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Write private key to file
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Create self-signed cert
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "TR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Istanbul"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Istanbul"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "AIS Demo"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)\
    .public_key(key.public_key())\
    .serial_number(x509.random_serial_number())\
    .not_valid_before(datetime.utcnow())\
    .not_valid_after(datetime.utcnow() + timedelta(days=365))\
    .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)\
    .sign(key, hashes.SHA256())

# Write cert to file
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ Certificate and key generated: cert.pem, key.pem")
