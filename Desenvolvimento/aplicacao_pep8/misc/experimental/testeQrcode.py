import qrcode


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

nome="bruna"
qr.add_data(f'testeando recebimento de qrcode {nome}')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('imgTeste.png')