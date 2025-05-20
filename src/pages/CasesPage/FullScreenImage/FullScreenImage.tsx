import React from 'react';
import styles from './styles.module.css';

interface FullscreenImageModalProps {
  images: string[];
  currentIndex: number;
  onClose: () => void;
  title?: string;
}

const FullscreenImageModal: React.FC<FullscreenImageModalProps> = ({
  images,
  currentIndex,
  onClose,
  title
}) => {
  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div 
        className={styles.modalContent} 
        onClick={(e) => e.stopPropagation()}
      >
        <button 
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close modal"
        >
          &times;
        </button>
        
        <img 
          src={images[currentIndex]} 
          alt={title || 'Fullscreen view'} 
          className={styles.fullscreenImage}
        />
      </div>
    </div>
  );
};

export default FullscreenImageModal;