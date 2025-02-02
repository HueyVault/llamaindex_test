from pyhwpx import Hwp  # 임포트


hwp = Hwp() 
filename = f'./documents/12091604_이상훈_arp_spoofing.hwp'
path = f'./documents'

hwp.open(filename=filename, format="", arg="")
# hwp.save_as(path=path, format="MSWORD", arg="")
hwp.save_pdf_as_image(path=path,img_format="bmp")

hwp.quit()

'''
            "MSWORD": 마이크로소프트 워드 문서
            "DOCRTF": MS 워드 문서 (doc)
            "OOXML": MS 워드 문서 (docx)
'''

'''
https://github.com/Jiayi-Pan/TinyZero/blob/main/tests/verl/utils/dataset/test_rl_dataset.py
'''

