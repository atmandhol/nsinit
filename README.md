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
kubectl apply -f pkg/install/default-rbac.yml
kapp deploy -a nsinit-repo -f pkg/install/packagerepo.yml
kapp deploy -a nsinit -f pkg/install/package.yml -y
```

### Packaging and releasing info

To publish:
- Change the image version in package-contents/config/config.yaml file to point to the right base image.
- Run these commands.
```bash
export VERSION=0.1.0
export IMAGE_REPO=adhol/nsinit
export BUNDLE_REPO=adhol/packages

docker build -t adhol/nsinit .
docker tag ${IMAGE_REPO}:latest ${IMAGE_REPO}:${VERSION}
docker push ${IMAGE_REPO}:${VERSION}

kbld -f pkg/contents/config/ --imgpkg-lock-output pkg/contents/.imgpkg/images.yml
ytt -f pkg/templates/package-template.yml --data-value-file openapi=pkg/templates/schema-openapi.yml -v version="${VERSION}" -v image=$(imgpkg push -b docker.io/${BUNDLE_REPO}:${VERSION} -f pkg/contents/ --json -y | jq '.Lines[-2]' | jq -r '.[8:-1]') > pkg/repo/packages/nsinit.adhol.io/${VERSION}.yml
cp pkg/templates/metadata.yml pkg/repo/packages/nsinit.adhol.io
kbld -f pkg/repo/packages/ --imgpkg-lock-output pkg/repo/.imgpkg/images.yml
imgpkg push -b docker.io/${BUNDLE_REPO}:${VERSION} -f pkg/repo
```

### Starlark Reference
https://github.com/bazelbuild/starlark/blob/master/spec.md