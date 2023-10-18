// ...

submitInformationBtn.addEventListener('click', function(event) {
  event.preventDefault();
  var companyId = document.getElementById('company_id').value;
  var nameOfCompany = document.getElementById('name_of_company').value;
  var companyType = document.getElementById('company_type').value;
  var website = document.getElementById('website').value;
  var location = document.getElementById('location').value;
  var moneySponsored = document.getElementById('money_sponsored').value;
  var contactEmail = document.getElementById('contact_email').value;
  var comments = document.getElementById('comments').value;

  fetch(`/block/${blockName}/add_information`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      company_id: companyId,
      name_of_company: nameOfCompany,
      company_type: companyType,
      website: website,
      location: location,
      money_sponsored: moneySponsored,
      contact_email: contactEmail,
      comments: comments
    })
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response if needed
    // For example, display a success message or update the UI
    // ...

    addInformationForm.reset();
    addInformationBtn.style.display = 'block';
    addInformationForm.style.display = 'none';
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

// ...


