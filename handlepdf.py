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
        print("Invalid argument, try python3 handlepdf.py -s path InitialPage1 FinalPage1 InitialPage2 FinalPage2 ... InitialPageN FinalPageN")
        exit()

    inputpdf = PdfFileReader(open(path, "rb"), strict=False)
    
    for rge in range(int(len(pages)/2)):
        initial_page = int(pages[rge*2])-1
        final_page = int(pages[rge*2+1])
    
        output_patt = path.replace('.pdf', '')

        output = PdfFileWriter()
        for pagenw in range(initial_page,final_page):
            output.addPage(inputpdf.getPage(pagenw))

        with open(output_patt + '_' + str(initial_page+1) + '_' + str(final_page) + '.pdf', "wb") as outputStream:
	        output.write(outputStream)
    print("PDF splitted successfully, please check the origin folder.")    

def join():
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import os

    global args

    output = PdfFileWriter()

    for path in args.vars:
        print(path)
        os.path.normpath(path)
        inputpdf = PdfFileReader(open(path, "rb"), strict=False)

        for pagenw in range(inputpdf.getNumPages()):
            output.addPage(inputpdf.getPage(pagenw))
    
    output_patt = args.vars[0][:args.vars[0].rfind('/')+1]

    with open(output_patt + 'JointPDF' + '.pdf', "wb") as outputStream:
	        output.write(outputStream)
    
    print("PDFs joint successfully, please check the first path folder.")


def joinsplit():
    print(2)

if args.split:
    split()
elif args.join:
    join()
elif args.joinsplit:
    joinsplit()
else:
    print("No command found, try -s for SplitPDF | -j for JoinPDF | -js for Join&SplitPDF")
