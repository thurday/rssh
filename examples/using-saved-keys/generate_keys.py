from Crypto.PublicKey import RSA

key_bits = 4096

new_key = RSA.generate(key_bits,e=65537)

private_key = new_key.exportKey('DER')
public_key = new_key.publickey().exportKey('DER')

with open('private.key','wb') as fd:
    fd.write(private_key)

with open('public.key','wb') as fd:
    fd.write(public_key)

print('Keys saved!')