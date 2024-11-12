document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("user-signup-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const firstName = document.getElementById("firstName").value;
        const lastName = document.getElementById("lastName").value;
        const age = document.getElementById("age").value;
        const gender = document.getElementById("gender").value;
        const zipcode = document.getElementById("zipcode").value;

        const userDetails = { firstName, lastName, age, gender, zipcode };

        try {
            // Send signup details to backend
            const response = await fetch("http://127.0.0.1:5000/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userDetails),
            });

            const result = await response.json();

            if (response.ok) {
                // Show success message and activate chatbot
                showNotification("User registered successfully! Activating chatbot...");
                activateChatbot(result.userId);
            } else {
                // Show error message
                showNotification(result.message);
            }
        } catch (error) {
            console.error("Error during signup:", error);
            showNotification("Something went wrong. Please try again.");
        }
    });

    async function activateChatbot(userId) {
        try {
            // Activate chatbot for registered user
            const response = await fetch("http://127.0.0.1:5000/activate-chatbot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ userId }),
            });

            const result = await response.json();

            if (response.ok) {
                showNotification(result.message);
                setTimeout(() => {
                    // Redirect to chat interface after activation
                    window.location.href = '/chat.html';  // Assuming you have a separate chat page
                }, 2000);
            } else {
                showNotification(result.message);
            }
        } catch (error) {
            console.error("Error activating chatbot:", error);
            showNotification("Failed to activate chatbot. Please try again.");
        }
    }

    // Show notification to user
    function showNotification(message) {
        const notification = document.createElement("div");
        notification.className = "notification";
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
});
