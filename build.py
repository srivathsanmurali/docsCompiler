import os
from os import listdir
from os.path import splitext
from shutil import copyfile
import pypandoc
import yaml

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

def main(srcs, outDir):
    indexLinks = []

    for name in srcs:
        path = srcs[name]['docSource']
        indexFile = srcs[name]['indexFile']

        if not os.path.exists(path):
            print()
            print("Source not available for", name)
            print("----------------------")
            continue

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

    indexString.append("\n## [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)")

    outIndexPath = outDir + "index.html"
    output = pypandoc.convert_text("\n".join(indexString),
                            'html5',
                            format="markdown")
    writeToHtml(output, outIndexPath)
    copyfile('pandoc.css', outDir + "pandoc.css")

    print("Indexfile Path =", outIndexPath)

def loadSources(filename):
    f = open(filename, 'r');
    srcs = yaml.safe_load(f)
    return srcs

if __name__ == "__main__":
    srcs = loadSources("./sources.yaml")
    main(srcs, "./build/")
