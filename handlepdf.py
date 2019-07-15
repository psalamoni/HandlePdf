import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--split", action="store_true")
group.add_argument("-j", "--join", action="store_true")
group.add_argument("-js", "--joinsplit", action="store_true")
parser.add_argument("vars", nargs="*", type=str)
args = parser.parse_args()

def split():
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import os
    
    global args

    path = args.vars[0]
    os.path.normpath(path)
    if all(x.isdigit() for x in args.vars[1:]) and len(args.vars[1:])%2==0:
        pages = args.vars[1:]
    else:
        print("Invalid argument")
        exit()

    inputpdf = PdfFileReader(open(path, "rb"), strict=False)
    
    for rge in range(int(len(pages)/2)):
        initial_page = int(pages[rge*2])-1
        final_page = int(pages[rge*2+1])
    
        output_patt = path.replace('.pdf', '')

        print("teste")

        output = PdfFileWriter()
        for pagenw in range(initial_page,final_page):
            output.addPage(inputpdf.getPage(pagenw))

        with open(output_patt + '_' + str(initial_page+1) + '_' + str(final_page) + '.pdf', "wb") as outputStream:
	        output.write(outputStream)    
    
    print (path)
    print (pages)

if args.split:
    split()
