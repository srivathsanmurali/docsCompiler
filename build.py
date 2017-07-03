import os
from os import listdir
from os.path import splitext
from shutil import copyfile
import pypandoc

### List of repos and its path
repos = [
        ('CalibrationTarget', 'src/CalibrationTarget/doc/', 'main.md'),
        ('openmvg', 'src/openmvg/docs/nomoko_docs/', 'documentation.markdown'),
        ('test', 'src/test/', 'test.md')
        ]

outDir = "./build/"

def writeToHtml(htmlText, filepath):
    htmlFile =  """<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="pandoc.css">
</head>
<body>
{0}
</body>
</html>
""".format(htmlText)
    with open(filepath, 'w') as f:
        f.write(htmlFile)

def main():
    indexLinks = []

    for (name, path, indexFile) in repos:
        print ("Processing" , name, "at", path)
        if not os.path.exists(outDir):
            os.makedirs(outDir)

        destDir = outDir + name + "/"
        if not os.path.exists(destDir):
            os.makedirs(destDir)
        copyfile('./pandoc.css', destDir +'pandoc.css')

        print()
        print("#####", name , "#####")
        print("Source Dir:", path)
        print("Destination Dir:", destDir)
        print("----------------------")
        for filename in listdir(path):
            src = path+filename
            if filename.endswith(".md") or filename.endswith(".markdown"):
                dest =  destDir + splitext(filename)[0] + ".html"
                print("pandoc", filename)
                output = pypandoc.convert_file( src,
                                                'html5',
                                                format="markdown")
                writeToHtml(output, dest)
            else:
                print("copy", filename)
                dest =  destDir + filename
                copyfile(src,dest)

        indexFilePath = "./" + name + "/" + splitext(indexFile)[0] + ".html"
        indexLinks.append((name, indexFilePath))
        print("Index file", indexFilePath)
        print("----------------------")

    indexString = ["# Nomoko Documentation"]
    for (n, i) in indexLinks:
        indexString.append("+ ["+n+"]("+i+")")

    outIndexPath = outDir + "index.html"
    output = pypandoc.convert_text("\n".join(indexString),
                            'html5',
                            format="markdown")
    writeToHtml(output, outIndexPath)
    copyfile('pandoc.css', outDir + "pandoc.css")

    print("Indexfile Path =", outIndexPath)

if __name__ == "__main__":
    main()