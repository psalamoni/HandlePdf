import argparse

parser = argparse.ArgumentParser()
batchtest = parser.add_mutually_exclusive_group()
group = parser.add_mutually_exclusive_group()
delete = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--split", action="store_true")
group.add_argument("-x", "--explode", action="store_true")
group.add_argument("-j", "--join", action="store_true")
group.add_argument("-js", "--joinsplit", action="store_true")
batchtest.add_argument("-b", "--batch", action="store_true")
delete.add_argument("-del", "--delete", action="store_true")
parser.add_argument("vars", nargs="*", type=str)
args = parser.parse_args()

def split(batch):
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import os
    
    global args

    args.vars = list(filter(None, args.vars))
    if len(args.vars)<=1:
        return
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
    
        if batch:
            output_patt = savepath
            name = path[path.rfind('/'):]
            name = name.replace('.pdf', '')
            output_patt = output_patt + name
        else:    
            output_patt = path.replace('.pdf', '')

        output = PdfFileWriter()
        for pagenw in range(initial_page,final_page):
            output.addPage(inputpdf.getPage(pagenw))

        with open(output_patt + '_' + str(initial_page+1) + '_' + str(final_page) + '.pdf', "wb") as outputStream:
	        output.write(outputStream)
    print("PDF splitted successfully, please check the origin folder.")    

def explode(batch):
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import os
    
    global args

    if len(args.vars)==0:
        return
    path = args.vars[0]
    os.path.normpath(path)

    inputpdf = PdfFileReader(open(path, "rb"), strict=False)

    if batch:
        output_patt = savepath
        name = path[path.rfind('/'):]
        name = name.replace('.pdf', '')
        output_patt = output_patt + name
    else:    
        output_patt = path.replace('.pdf', '')
    
    for pagenw in range(inputpdf.getNumPages()):
        
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(pagenw))

        with open(output_patt + '_' + str(pagenw+1) + '.pdf', "wb") as outputStream:
	        output.write(outputStream)
        
    if args.delete:
        os.remove(path)
    print("PDF splitted successfully, please check the origin folder.")

def join():
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import os

    global args

    output = PdfFileWriter()

    for path in args.vars:
        try:
            os.path.normpath(path)
            inputpdf = PdfFileReader(open(path, "rb"), strict=False)
        except:
            print("Invalid path, try python3 handlepdf.py -j 'path1' 'path2' ... 'pathn'")

        for pagenw in range(inputpdf.getNumPages()):
            output.addPage(inputpdf.getPage(pagenw))
    
    output_patt = args.vars[0][:args.vars[0].rfind('/')+1]

    with open(output_patt + 'JointPDF' + '.pdf', "wb") as outputStream:
	        output.write(outputStream)
    
    print("PDFs joint successfully, please check the first path folder.")

def joinsplit():
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import os

    global args

    if len(args.vars)%3==0:

        output = PdfFileWriter()

        for rge in range(int(len(args.vars)/3)):

            path = args.vars[rge*3]
            try:
                os.path.normpath(path)
                inputpdf = PdfFileReader(open(path, "rb"), strict=False)
            except:
                print("Invalid path, try python3 handlepdf.py -js 'path1' InitialPage1 FinalPage1 'path2' InitialPage2 FinalPage2 ... 'pathN' InitialPageN FinalPageN")

            initial_page = args.vars[rge*3+1]
            final_page = args.vars[rge*3+2]

            if initial_page.isdigit() and final_page.isdigit():

                initial_page = int(initial_page)-1
                final_page = int(final_page)

                for pagenw in range(initial_page,final_page):
                    output.addPage(inputpdf.getPage(pagenw))

            else:
                print("Invalid page number, try python3 handlepdf.py -js 'path1' InitialPage1 FinalPage1 'path2' InitialPage2 FinalPage2 ... 'pathN' InitialPageN FinalPageN")

        output_patt = args.vars[0][:args.vars[0].rfind('/')+1]
        
        with open(output_patt + 'SplitJointPDF' + '.pdf', "wb") as outputStream:
	        output.write(outputStream)
        
        print("PDFs joint successfully, please check the first path folder.")

    else:
        print("Invalid argument, try python3 handlepdf.py -js 'path1' InitialPage1 FinalPage1 'path2' InitialPage2 FinalPage2 ... 'pathN' InitialPageN FinalPageN")
        exit()

if args.batch:
    import os
    import csv

    batchcsv = args.vars[1:]
    pathcsv = args.vars[0]
    savepath = None
    if len(args.vars)>1:
        savepath = args.vars[1]
    os.path.normpath(pathcsv)

    with open(pathcsv, 'r') as f:
        reader = csv.reader(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        paths = list(reader)

    if args.split:
        for newarg in paths:
            print (newarg)
            args.vars = newarg
            if savepath==None:
                split(False)
            else:
                split(True)
    elif args.explode:
        for newarg in paths:
            print (newarg)
            args.vars = newarg
            if savepath==None:
                explode(False)
            else:
                explode(True)    
    elif args.join:
        args = paths
        join()
    else:
        print("No command found, try -b -s for batch SplitPDF | -b -j for batch JoinPDF | no Join&SplitPDF for batch file supported")
else:
    if args.split:
        split(False)
    elif args.join:
        join()
    elif args.joinsplit:
        joinsplit()
    else:
        print("No command found, try -s for SplitPDF | -j for JoinPDF | -js for Join&SplitPDF")
