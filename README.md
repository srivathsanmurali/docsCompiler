# DOCS compiler

## dependencies

+ python35
  * pypandoc
  * pyyaml
+ pandoc

## nixos
```
nix-shell -p python35Full python35Packages.pypandoc python35Packages.pyyaml pandoc --run "python build.py"
```

## yaml file format
```
[folder-name]
  docSource: [doc-source]
  indexFile: [index-file]
[folder-name]
  docSource: [doc-source]
  indexFile: [index-file]
[folder-name]
  docSource: [doc-source]
  indexFile: [index-file]
```
