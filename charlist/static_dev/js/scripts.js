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


function handleFooterClick() {
    clickCount++;
    if (clickCount === 5) {
        const messageText = "The glorious heroes of Eberron, who saved the world from the great evil in the person of Zor'Fael: Kurt, Starley, Theo, Arannis";
        document.getElementById("my-session-header").innerText = messageText;
    }
}


