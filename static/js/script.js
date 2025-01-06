function completaTurno(index) {
    fetch("/completa", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ index: index }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Errore nel completamento del turno.");
            }
        });
}
