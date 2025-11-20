import React from "react";

export default function Privacy() {
  return (
    <div className="flex items-center justify-center flex-1 px-6 bg-primary-50">
      <div className="w-full max-w-md mb-20 space-y-4 text-center text-white">
        <h1 className="text-2xl font-bold">Politique de Confidentialité</h1>
        <p>Dernière mise à jour : 20/11</p>

        <h2 className="text-lg font-semibold">1. Données collectées</h2>
        <p>
          Nous collectons uniquement les données nécessaires : adresse e-mail,
          mot de passe haché, date de création du compte, conversations,
          messages, guides, sources et tags.
        </p>

        <h2 className="text-lg font-semibold">2. Utilisation des données</h2>
        <p>
          Vos données servent uniquement à gérer votre compte, sauvegarder vos
          conversations, afficher le contenu et améliorer l&apos;application.
        </p>

        <h2 className="text-lg font-semibold">3. Sécurité</h2>
        <p>
          Les mots de passe sont hachés et l&apos;accès aux bases de données est
          sécurisé, mais aucun système n&apos;est infaillible.
        </p>

        <h2 className="text-lg font-semibold">4. Partage des données</h2>
        <p>
          Aucune donnée n&apos;est partagée sauf obligation légale ou judiciaire.
        </p>

        <h2 className="text-lg font-semibold">5. Durée de conservation</h2>
        <p>Les données sont conservées tant que votre compte est actif.</p>

        <h2 className="text-lg font-semibold">6. Vos droits</h2>
        <p>
          Vous pouvez demander l&apos;accès, la rectification ou la suppression de
          vos données via : [insérer e-mail].
        </p>

        <h2 className="text-lg font-semibold">7. Modification</h2>
        <p>
          La politique peut être mise à jour, et la date de modification sera
          indiquée.
        </p>
      </div>
    </div>
  );
}