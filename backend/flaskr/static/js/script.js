document.addEventListener("DOMContentLoaded", function () {
  const starsContainer = document.querySelectorAll(".stars");

  starsContainer.forEach((container) => {
    const rating = parseFloat(container.getAttribute("data-rating"));
    const stars = container.querySelectorAll(".star");

    // 计算涂色宽度
    let filledStars = Math.floor(rating / 2);
    let remainder = (rating % 2) / 2;

    stars.forEach((star, index) => {
      if (index < filledStars) {
        star.style.color = "#FFD700"; // 完全涂色
      } else if (index === filledStars && remainder > 0) {
        star.style.width = `${remainder * 100}%`; // 部分涂色
      }
    });
  });
});

function openReportModal(entryId) {
  document.getElementById("reportEntryId").value = entryId;
  document.getElementById("reportModal").style.display = "flex";
}

function closeReportModal() {
  document.getElementById("reportModal").style.display = "none";
}

function openBlockModal(entryId) {
  document.getElementById("blockEntryId").value = entryId;
  document.getElementById("blockModal").style.display = "flex";
}

function closeBlockModal() {
  document.getElementById("blockModal").style.display = "none";
}

function openReportCommentModal(commentId) {
  document.getElementById("reportCommentId").value = commentId;
  document.getElementById("reportCommentModal").style.display = "flex";
}

function closeReportCommentModal() {
  document.getElementById("reportCommentModal").style.display = "none";
}

function openBlockCommentModal(commentId) {
  document.getElementById("blockCommentId").value = commentId;
  document.getElementById("blockCommentId").style.display = "flex";
}

function closeBlockCommentModal() {
  document.getElementById("blockCommentModal").style.display = "none";
}

function switchTab(tabId) {
  const tabs = document.querySelectorAll(".tab-content");
  tabs.forEach((tab) => tab.classList.remove("active"));
  document.getElementById(tabId).classList.add("active");
}

function openModal(formId) {
  document.getElementById("modal").style.display = "flex";
  document
    .querySelectorAll(".modal-content > div")
    .forEach((div) => (div.style.display = "none"));
  document.getElementById(formId + "-form").style.display = "block";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}
