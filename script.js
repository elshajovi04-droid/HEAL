document.addEventListener("DOMContentLoaded", function () {

    const input = document.querySelector(".input-area input");
    const button = document.querySelector(".input-area button");
    const chat = document.querySelector(".chat-messages");


    // =========================
    // Get Current Time
    // =========================

    function getTime() {

        const now = new Date();

        return now.toLocaleTimeString([], {
            hour: "numeric",
            minute: "2-digit"
        });
    }


    // =========================
    // Add User Message
    // =========================

    function addUserMessage(text) {

        const userRow = document.createElement("div");
        userRow.className = "message-row user-row";

        const userContent = document.createElement("div");

        const userMessage = document.createElement("div");
        userMessage.className = "message user-message";
        userMessage.textContent = text;

        const userTime = document.createElement("div");
        userTime.className = "time user-time";
        userTime.textContent = getTime();

        userContent.appendChild(userMessage);
        userContent.appendChild(userTime);


        const userAvatar = document.createElement("div");
        userAvatar.className = "avatar";
        userAvatar.textContent = "👤";


        userRow.appendChild(userContent);
        userRow.appendChild(userAvatar);

        chat.appendChild(userRow);

        chat.scrollTop = chat.scrollHeight;
    }


    // =========================
    // Add HEAL Message
    // =========================

    function addHealMessage(text) {

        const healRow = document.createElement("div");
        healRow.className = "message-row heal-row";


        const healAvatar = document.createElement("div");
        healAvatar.className = "avatar";
        healAvatar.textContent = "🐧";


        const healContent = document.createElement("div");


        const healMessage = document.createElement("div");
        healMessage.className = "message heal-message";
        healMessage.textContent = text;


        const healTime = document.createElement("div");
        healTime.className = "time heal-time";
        healTime.textContent = getTime();


        healContent.appendChild(healMessage);
        healContent.appendChild(healTime);


        healRow.appendChild(healAvatar);
        healRow.appendChild(healContent);

        chat.appendChild(healRow);

        chat.scrollTop = chat.scrollHeight;
    }


    // =========================
    // Send Message
    // =========================

    async function sendMessage() {

        const text = input.value.trim();


        if (text === "") {
            return;
        }


        // Show user's message
        addUserMessage(text);

        // Clear input
        input.value = "";

        // Disable button while HEAL is responding
        button.disabled = true;


        try {

            // =========================
            // Send Message to Flask
            // =========================

            const response = await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: text
                })

            });


            // Check server response
            if (!response.ok) {
                throw new Error("Server error");
            }


            const data = await response.json();


            // =========================
            // Display NLP Response
            // =========================

            if (data.reply) {

                addHealMessage(data.reply);

            } else {

                addHealMessage(
                    "I'm here with you, buddy 💗"
                );

            }


            // Console shows NLP analysis
            console.log("HEAL NLP:");
            console.log("Emotion:", data.emotion);
            console.log("Intent:", data.intent);

        }


        catch (error) {

            console.error("Backend error:", error);

            addHealMessage(
                "Something went wrong, buddy. Please try again 💗"
            );

        }


        // Enable button again
        button.disabled = false;

        input.focus();
    }


    // =========================
    // Send Button
    // =========================

    button.addEventListener("click", sendMessage);


    // =========================
    // Enter Key
    // =========================

    input.addEventListener("keypress", function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    });

});