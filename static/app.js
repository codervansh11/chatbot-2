class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;
        chatbox.classList.toggle('chatbox--active', this.state);
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        let text1 = textField.value.trim();

        if (!text1) return;

        this.messages.push({ name: "User", message: text1 });
        this.updateChatText(chatbox);
        textField.value = '';

        fetch(`${window.location.origin}/predict`, {
            method: 'POST',
            body: JSON.stringify({ messages: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            this.messages.push({ name: "Sam", message: data.answer || "No response received." });
            this.updateChatText(chatbox);
        })
        .catch(error => {
            console.error("Error:", error);
            this.messages.push({ name: "Sam", message: "Oops! Something went wrong." });
            this.updateChatText(chatbox);
        });
    }

    updateChatText(chatbox) {
        const chatMessages = chatbox.querySelector('.chatbox__messages');
        chatMessages.innerHTML = this.messages.slice().reverse().map(item => {
            return `<div class="messages__item messages__item--${item.name === "Sam" ? "visitor" : "operator"}">${item.message}</div>`;
        }).join('');
    }
}

const chatbox = new Chatbox();
chatbox.display();
