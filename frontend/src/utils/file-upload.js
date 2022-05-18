function upload(formData) {
  const image = formData.getAll("images")[0];
  const promise = getBase64Image(image);
  return promise;
}

function getBase64Image(file) {
  return new Promise((resolve) => {
    const fReader = new FileReader();

    fReader.onload = () => {
      return resolve(fReader.result);
    };

    fReader.onerror = () => {
      return resolve(undefined);
    };

    fReader.readAsDataURL(file);
  });
}

export { upload };
