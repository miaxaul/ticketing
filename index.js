document.addEventListener("DOMContentLoaded", () => {
    // Tab navigation functionality
    const tabs = document.querySelectorAll(".tab-button");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const target = tab.dataset.tab;

            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(content => content.classList.remove("active"));

            tab.classList.add("active");
            document.getElementById(target).classList.add("active");
        });
    });

    // API base URL (Replace with your actual API endpoint)
    const API_BASE_URL = "https://mr04w2vlta.execute-api.us-east-1.amazonaws.com/prod"; // Replace with the correct API Gateway URL

    /**
     * Handle Order Form Submission
     */
    const orderForm = document.getElementById("orderForm");
    const orderOutput = document.getElementById("orderOutput");

    orderForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const movieName = document.getElementById("movieName").value;
        const userId = document.getElementById("userId").value;
        const ticketQuantity = parseInt(document.getElementById("ticketQuantity").value, 10);

        const payload = {
            movie_name: movieName,
            user_id: userId,
            ticket_quantity: ticketQuantity
        };

        try {
            const response = await fetch(`${API_BASE_URL}/order`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            orderOutput.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            orderOutput.textContent = `Error: ${error.message}`;
        }
    });

    /**
     * Handle Payment Form Submission
     */
    const paymentForm = document.getElementById("paymentForm");
    const paymentOutput = document.getElementById("paymentOutput");

    paymentForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const token = document.getElementById("paymentToken").value;
        const price = parseInt(document.getElementById("paymentPrice").value, 10);

        const payload = {
            token: token,
            price: price
        };

        try {
            const response = await fetch(`${API_BASE_URL}/payment`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            paymentOutput.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            paymentOutput.textContent = `Error: ${error.message}`;
        }
    });

    /**
     * Handle Get Tickets Request
     */
    const getTicketsButton = document.getElementById("getTickets");
    const ticketOutput = document.getElementById("ticketOutput");

    getTicketsButton.addEventListener("click", async () => {
        const userId = document.getElementById("queryUserId").value;

        if (!userId) {
            ticketOutput.textContent = "Error: User ID is required to fetch tickets.";
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/tickets?user_id=${encodeURIComponent(userId)}`, {
                method: "GET"
            });

            const data = await response.json();
            ticketOutput.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            ticketOutput.textContent = `Error: ${error.message}`;
        }
    });
});
