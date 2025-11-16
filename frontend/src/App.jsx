import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';

export default function App() {
  const [searchValue, setSearchValue] = useState('');
  const [opacity, setOpacity] = useState(1);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // List of influential politicians and individuals
  const influentialPeople = [
    'Donald Trump',
    'Elon Musk',
    'Joe Biden',
    'Kamala Harris',
    'Barack Obama',
    'Vladimir Putin',
    'Xi Jinping',
    'Jeff Bezos',
    'Bill Gates',
    'Mark Zuckerberg',
    'Warren Buffett',
    'Bernie Sanders',
    'Ron DeSantis',
    'Nancy Pelosi',
    'Mitch McConnell',
    'Alexandria Ocasio-Cortez',
    'Mike Pence',
    'Nikki Haley',
    'Vivek Ramaswamy',
    'Robert F. Kennedy Jr.',
    'Tim Cook',
    'Sundar Pichai',
    'Sam Altman',
    'Larry Page',
    'Sergey Brin',
    'Peter Thiel',
    'Marc Andreessen',
    'Reid Hoffman',
    'Jack Dorsey',
    'Brian Armstrong'
  ];

  useEffect(() => {
  // Only fade if search bar is empty
  if (searchValue.trim() !== '') {
    setOpacity(1);
    return;
  }

  let direction = -1;
  
  const interval = setInterval(() => {
    setOpacity(prev => {
      const newOpacity = prev + (direction * 0.02);
      
      if (newOpacity <= 0.3) {
        direction = 1;
        return 0.3;
      }
      if (newOpacity >= 1) {
        direction = -1;
        return 1;
      }
      
      return newOpacity;
    });
  }, 50);

  return () => clearInterval(interval);
}, [searchValue]); 

  // Filter suggestions based on search input
  useEffect(() => {
    if (searchValue.trim() === '') {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    const filtered = influentialPeople.filter(person =>
      person.toLowerCase().includes(searchValue.toLowerCase())
    ).slice(0, 6); // Limit to 6 suggestions

    setSuggestions(filtered);
    setShowSuggestions(filtered.length > 0);
  }, [searchValue]);

  const handleSuggestionClick = (person) => {
    setSearchValue(person);
    setShowSuggestions(false);
    // Navigate to person's page
    const urlName = person.toLowerCase().replace(/\s+/g, '-');
    window.location.href = `/person/${urlName}`;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && searchValue.trim()) {
      setShowSuggestions(false);
      // Navigate to person's page
      const urlName = searchValue.toLowerCase().replace(/\s+/g, '-');
      window.location.href = `/person/${urlName}`;
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      width: '100vw',
      background: 'linear-gradient(to bottom right, #18181b, #57534e, #262626)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      overflow: 'hidden',
      margin: 0,
      padding: 0,
      boxSizing: 'border-box'
    },
    backgroundPattern: {
      position: 'absolute',
      inset: 0,
      opacity: 0.1,
      backgroundImage: `repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(156, 163, 175, 0.1) 2px,
        rgba(156, 163, 175, 0.1) 4px
      )`
    },
    content: {
      zIndex: 10,
      width: '100%',
      maxWidth: '56rem',
      padding: '0 1.5rem'
    },
    title: {
      fontFamily: 'Raleway, sans-serif',
      fontWeight: 200,
      fontSize: 'clamp(3rem, 8vw, 6rem)',
      textAlign: 'center',
      marginBottom: '4rem',
      textTransform: 'uppercase',
      transform: 'scaleX(1.6)',
      background: 'linear-gradient(135deg, #e5e5e5 0%, #a3a3a3 50%, #d4d4d4 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text',
      textShadow: '0 0 40px rgba(229, 229, 229, 0.2)',
      letterSpacing: '0.2em'
    },
    searchContainer: {
      position: 'relative',
      opacity: opacity
    },
    searchWrapper: {
      position: 'relative'
    },
    searchGlow: {
      position: 'absolute',
      inset: '-4px',
      background: 'linear-gradient(to right, #52525b, #9ca3af, #52525b)',
      borderRadius: '1rem',
      filter: 'blur(8px)',
      opacity: 0.25,
      transition: 'opacity 0.5s'
    },
    searchBox: {
      position: 'relative',
      display: 'flex',
      alignItems: 'center',
      background: 'linear-gradient(to right, #27272a, #262626)',
      borderRadius: '1rem',
      border: '1px solid #52525b',
      boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      overflow: 'hidden'
    },
    searchIcon: {
      marginLeft: '1.5rem',
      color: '#9ca3af',
      flexShrink: 0
    },
    input: {
      width: '100%',
      padding: '1.5rem',
      background: 'transparent',
      color: '#e5e7eb',
      border: 'none',
      outline: 'none',
      letterSpacing: '0.2em',
      textTransform: 'uppercase',
      fontSize: '1.125rem',
      fontFamily: 'Orbitron, monospace',
      transform: 'scaleX(1.3)',
      transformOrigin: 'left'
    },
    divider: {
      height: '3rem',
      width: '1px',
      background: 'linear-gradient(to bottom, transparent, #6b7280, transparent)',
      marginRight: '1rem'
    },
    suggestionsBox: {
      position: 'absolute',
      top: 'calc(100% + 0.5rem)',
      left: 0,
      right: 0,
      background: 'linear-gradient(to bottom, #27272a, #1c1c1e)',
      border: '1px solid #52525b',
      borderRadius: '0.75rem',
      boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      overflow: 'hidden',
      zIndex: 50
    },
    suggestion: {
      padding: '1rem 1.5rem',
      color: '#e5e7eb',
      cursor: 'pointer',
      transition: 'background 0.2s',
      fontFamily: 'Orbitron, monospace',
      fontSize: '0.95rem',
      borderBottom: '1px solid #3f3f46'
    }
  };

  return (
    <>
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        body {
          margin: 0;
          padding: 0;
          overflow-x: hidden;
        }
        #root {
          margin: 0;
          padding: 0;
        }
      `}</style>
      
      <div style={styles.container}>
        <div style={styles.backgroundPattern} />

        <div style={styles.content}>
          <h1 style={styles.title}>
            HARKONNEN
          </h1>

          <div style={styles.searchContainer}>
            <div style={styles.searchWrapper}>
              <div style={styles.searchGlow} />
              
              <div style={styles.searchBox}>
                <div style={styles.searchIcon}>
                  <Search size={24} />
                </div>
                
                <input
                  type="text"
                  value={searchValue}
                  onChange={(e) => setSearchValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  onFocus={() => searchValue && setShowSuggestions(true)}
                  placeholder="INITIALIZE SEARCH PROTOCOL..."
                  style={styles.input}
                  autoComplete="off"
                />

                <div style={styles.divider} />
              </div>

              {/* Suggestions dropdown */}
              {showSuggestions && suggestions.length > 0 && (
                <div style={styles.suggestionsBox}>
                  {suggestions.map((person, index) => (
                    <div
                      key={index}
                      style={styles.suggestion}
                      onClick={() => handleSuggestionClick(person)}
                      onMouseEnter={(e) => e.target.style.background = '#3f3f46'}
                      onMouseLeave={(e) => e.target.style.background = 'transparent'}
                    >
                      {person}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Raleway:wght@200;300&display=swap" rel="stylesheet" />
      </div>
    </>
  );
}