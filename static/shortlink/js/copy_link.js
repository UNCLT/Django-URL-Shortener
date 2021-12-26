$('document').ready(function () {

    const copyBtns = [...document.getElementsByClassName('copy-btn')];

    let previous = null

    copyBtns.forEach(btn => btn.addEventListener('click', () => {
        const linkToCopy = 'https://ya.link/' + btn.getAttribute('data-link')
        navigator.clipboard.writeText(linkToCopy)
        btn.textContent = 'Copied!'

        if (previous) {
            previous.textContent = 'Copy'
        }
        previous = btn
    }))

});

