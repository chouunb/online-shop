document.addEventListener("click", async (event) => {

    const button = event.target.closest(".delete-review-btn");

    if (!button) return;

    const reviewId = button.dataset.reviewId;
    const deleteUrl = button.dataset.deleteUrl;

    const confirmed = confirm(
        "Удалить отзыв?"
    );

    if (!confirmed) return;

    try {

        const response = await fetch(deleteUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            }
        });

        const data = await response.json();

        if (data.success) {

            const reviewElement =
                document.getElementById(
                    `review-${reviewId}`
                );

            reviewElement.remove();

        }

    } catch (error) {

        console.error(error);

    }

});

function getCSRFToken() {

    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];

}