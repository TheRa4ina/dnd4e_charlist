function copyToClipboard(button, url) {
    navigator.clipboard.writeText(url).then(
      () => {
        button.innerText = 'Copied!';
        setTimeout(() => {
          button.innerText = 'Copy Invite Link';
        }, 2000);
      },
      err => console.error('Could not copy text: ', err)
    );
  }
