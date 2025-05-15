import React, { useState, useCallback } from "react";
import Modal from "../components/Modal";

let externalShowModal;

export function ModalProvider({ children }) {
  const [modalConfig, setModalConfig] = useState(null);

  const showModal = useCallback(() => {
    return new Promise((resolve, reject) => {
      setModalConfig({
        onSubmit: (data) => {
          setModalConfig(null);
          resolve(data);
        },
        onCancel: () => {
          setModalConfig(null);
          reject(new Error("Modal cancelled"));
        },
      });
    });
  }, []);

  externalShowModal = showModal;

  return (
    <>
      {children}
      {modalConfig && <Modal {...modalConfig} />}
    </>
  );
}

// Exported function to use anywhere in the app
export function showModal() {
  if (!externalShowModal) {
    throw new Error("ModalProvider not mounted");
  }
  return externalShowModal();
}
