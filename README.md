## nsinit

Kubernetes namespace initialization controller.

### Instructions to run this controller
This controller uses carvel tools for packaging.

Install kapp-controller
```bash
kapp deploy -a kc -f https://github.com/vmware-tanzu/carvel-kapp-controller/releases/download/v0.32.0/release.yml -y
```
Install package repo and package
```bash
kapp deploy -a nsinit -f install.yml -y
```

### Packaging and releasing info

To push the version bundle:
- Do a Docker build and push the image to Dockerhub.
- Change the image version in package-contents/config/config.yaml file to point to the right base image.
- Run these commands.
```bash
kbld -f package-contents/config/ --imgpkg-lock-output package-contents/.imgpkg/images.yml
imgpkg push -b docker.io/adhol/nsinit:${VERSION} -f package-contents/
```
Create a package entry in the repo bundle
```bash
ytt -f templates/package-template.yml  --data-value-file openapi=templates/schema-openapi.yml -v version="${VERSION}" > my-pkg-repo/packages/nsinit.adhol.io/${VERSION}.yml
cp templates/metadata.yml my-pkg-repo/packages/nsinit.adhol.io
```
Push the repo bundle
```bash
kbld -f my-pkg-repo/packages/ --imgpkg-lock-output my-pkg-repo/.imgpkg/images.yml
imgpkg push -b docker.io/adhol/nsinit:${VERSION} -f my-pkg-repo
```

### Starlark Reference
https://github.com/bazelbuild/starlark/blob/master/spec.md