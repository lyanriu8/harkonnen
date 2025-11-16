import { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Heart, Repeat2, ChevronDown } from 'lucide-react';

export default function PersonPage() {
  // For demo purposes - in your real app, use useParams() from react-router-dom
  const name = 'donald-trump';
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [likedPosts, setLikedPosts] = useState(new Set());
  const [repostedPosts, setRepostedPosts] = useState(new Set());
  const [sortBy, setSortBy] = useState('newest');
  const [dropdownOpen, setDropdownOpen] = useState(false);

/*
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Heart, Repeat2 } from 'lucide-react';

export default function PersonPage() {
  const { name } = useParams();  // Get name from URL
  const navigate = useNavigate();  // For navigation
  
  // ... rest of the code from the artifact, but replace:
  // - window.location.href = '/' with navigate('/')
  // - Remove the hardcoded name = 'donald-trump'
  // - Replace mock data with actual API call:
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/person/${name}`);
        const result = await response.json();
        setData(result);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };
    fetchData();
  }, [name]);
  
  // ... rest stays the same
}
*/

// could make a about page
// 



  
  // Convert URL name back to display name
  const displayName = name
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');

  const dropdownRef = useRef(null);

  const sortOptions = [
    { value: 'newest', label: 'Newest' },
    { value: 'oldest', label: 'Oldest' },
    { value: '1day-positive', label: 'Positive 1-Day Change' },
    { value: '7day-positive', label: 'Positive 7-Day Change' },
    { value: '1day-negative', label: 'Negative 1-Day Change' },
    { value: '7day-negative', label: 'Negative 7-Day Change' }
  ];

  const handleSortChange = (value) => {
    setSortBy(value);
    setDropdownOpen(false);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    // Mock data for demo - in your real app, fetch from backend
    const mockData = {
      one_day_influence_score: 87.5,
      seven_day_influence_score: 92.3,
      posts: [
        {
          post_id: '1',
          timestamp: '2024-11-15T10:30:00Z',
          username: 'realDonaldTrump',
          content: 'Just announced major policy changes that will revolutionize the tech industry. Big things coming!',
          sentiment: { positive: 0.8, negative: 0.1, neutral: 0.1 },
          tickers: ['TSLA', 'AAPL'],
          price_changes: [
            { ticker: 'TSLA', one_day: 5.2, seven_day: 12.8, one_day_percent: 2.3, seven_day_percent: 5.8 },
            { ticker: 'AAPL', one_day: 3.1, seven_day: 8.5, one_day_percent: 1.8, seven_day_percent: 4.9 }
          ]
        },
        {
          post_id: '2',
          timestamp: '2024-11-14T15:45:00Z',
          username: 'realDonaldTrump',
          content: 'Meeting with major industry leaders tomorrow. Exciting developments ahead for American businesses!',
          sentiment: { positive: 0.9, negative: 0.05, neutral: 0.05 },
          tickers: ['NVDA', 'MSFT'],
          price_changes: [
            { ticker: 'NVDA', one_day: -2.1, seven_day: 3.2, one_day_percent: -0.5, seven_day_percent: 0.8 },
            { ticker: 'MSFT', one_day: 1.8, seven_day: 6.3, one_day_percent: 0.4, seven_day_percent: 1.5 }
          ]
        },
        {
          post_id: '3',
          timestamp: '2024-11-13T09:20:00Z',
          username: 'realDonaldTrump',
          content: 'The stock market is showing tremendous strength. America is winning again!',
          sentiment: { positive: 0.95, negative: 0.0, neutral: 0.05 },
          tickers: ['SPY', 'QQQ'],
          price_changes: [
            { ticker: 'SPY', one_day: 4.5, seven_day: 15.2, one_day_percent: 1.1, seven_day_percent: 3.6 },
            { ticker: 'QQQ', one_day: 6.8, seven_day: 18.9, one_day_percent: 1.8, seven_day_percent: 5.1 }
          ]
        }
      ]
    };

    // Simulate API call
    setTimeout(() => {
      setData(mockData);
      setLoading(false);
    }, 500);
  }, []);

  const toggleLike = (postId) => {
    setLikedPosts(prev => {
      const newSet = new Set(prev);
      if (newSet.has(postId)) {
        newSet.delete(postId);
      } else {
        newSet.add(postId);
      }
      return newSet;
    });
  };

  const toggleRepost = (postId) => {
    setRepostedPosts(prev => {
      const newSet = new Set(prev);
      if (newSet.has(postId)) {
        newSet.delete(postId);
      } else {
        newSet.add(postId);
      }
      return newSet;
    });
  };

  const formatPercent = (value) => {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
  };

  const getPercentColor = (value) => {
    return value >= 0 ? '#10b981' : '#ef4444';
  };

  const getSortedPosts = () => {
    if (!data || !data.posts) return [];
    
    const posts = [...data.posts];
    
    switch(sortBy) {
      case 'newest':
        return posts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      
      case 'oldest':
        return posts.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
      
      case '1day-positive':
        return posts.sort((a, b) => {
          const aMax = Math.max(...a.price_changes.map(p => p.one_day_percent));
          const bMax = Math.max(...b.price_changes.map(p => p.one_day_percent));
          return bMax - aMax;
        });
      
      case '7day-positive':
        return posts.sort((a, b) => {
          const aMax = Math.max(...a.price_changes.map(p => p.seven_day_percent));
          const bMax = Math.max(...b.price_changes.map(p => p.seven_day_percent));
          return bMax - aMax;
        });
      
      case '1day-negative':
        return posts.sort((a, b) => {
          const aMin = Math.min(...a.price_changes.map(p => p.one_day_percent));
          const bMin = Math.min(...b.price_changes.map(p => p.one_day_percent));
          return aMin - bMin;
        });
      
      case '7day-negative':
        return posts.sort((a, b) => {
          const aMin = Math.min(...a.price_changes.map(p => p.seven_day_percent));
          const bMin = Math.min(...b.price_changes.map(p => p.seven_day_percent));
          return aMin - bMin;
        });
      
      default:
        return posts;
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      width: '100%',
      background: 'linear-gradient(to bottom right, #18181b, #57534e, #262626)',
      padding: '2rem',
      color: '#e5e7eb',
      boxSizing: 'border-box',
      margin: 0
    },
    backButton: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      background: 'transparent',
      border: '1px solid #52525b',
      color: '#e5e7eb',
      padding: '0.75rem 1.5rem',
      borderRadius: '0.5rem',
      cursor: 'pointer',
      fontSize: '1rem',
      fontFamily: 'Orbitron, monospace',
      marginBottom: '2rem'
    },
    header: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '3rem',
      flexWrap: 'wrap',
      gap: '2rem',
      padding: '2rem',
      background: 'linear-gradient(to right, #27272a, #262626)',
      borderRadius: '1rem',
      border: '1px solid #52525b'
    },
    name: {
      fontFamily: 'Raleway, sans-serif',
      fontSize: 'clamp(2rem, 5vw, 3.5rem)',
      fontWeight: 200,
      textTransform: 'uppercase',
      letterSpacing: '0.2em',
      background: 'linear-gradient(135deg, #e5e5e5 0%, #a3a3a3 50%, #d4d4d4 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      flex: '1 1 300px'
    },
    scoresContainer: {
      display: 'flex',
      gap: '3rem',
      flexWrap: 'wrap'
    },
    scoreBox: {
      textAlign: 'center'
    },
    scoreLabel: {
      fontFamily: 'Orbitron, monospace',
      fontSize: '0.75rem',
      color: '#9ca3af',
      letterSpacing: '0.1em',
      marginBottom: '0.5rem',
      textTransform: 'uppercase'
    },
    scoreValue: {
      fontFamily: 'Orbitron, monospace',
      fontSize: '2rem',
      fontWeight: 'bold',
      color: '#e5e7eb'
    },
    postsContainer: {
      maxWidth: '1200px',
      margin: '0 auto'
    },
    sortContainer: {
      display: 'flex',
      justifyContent: 'flex-end',
      marginBottom: '2rem',
      gap: '1rem',
      alignItems: 'center',
      position: 'relative'
    },
    sortLabel: {
      fontFamily: 'Orbitron, monospace',
      fontSize: '0.875rem',
      color: '#9ca3af',
      letterSpacing: '0.1em',
      textTransform: 'uppercase'
    },
    customSelect: {
      position: 'relative',
      width: '320px'
    },
    selectButton: {
      fontFamily: 'Orbitron, monospace',
      fontSize: '0.875rem',
      padding: '0.75rem 1.5rem',
      background: 'linear-gradient(to right, #27272a, #262626)',
      border: '1px solid #52525b',
      borderRadius: '1rem',
      color: '#e5e7eb',
      cursor: 'pointer',
      outline: 'none',
      transition: 'all 0.3s',
      letterSpacing: '0.05em',
      textTransform: 'uppercase',
      width: '100%',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    dropdownMenu: {
      position: 'absolute',
      top: 'calc(100% + 0.5rem)',
      left: 0,
      right: 0,
      background: 'linear-gradient(to bottom, #27272a, #1c1c1e)',
      border: '1px solid #52525b',
      borderRadius: '1rem',
      boxShadow: '0 10px 40px rgba(0, 0, 0, 0.5)',
      overflow: 'hidden',
      zIndex: 100
    },
    dropdownOption: {
      fontFamily: 'Orbitron, monospace',
      fontSize: '0.875rem',
      padding: '0.75rem 1.5rem',
      color: '#e5e7eb',
      cursor: 'pointer',
      transition: 'background 0.2s',
      letterSpacing: '0.05em',
      textTransform: 'uppercase',
      borderBottom: '1px solid #3f3f46'
    },
    post: {
      display: 'flex',
      gap: '2rem',
      background: 'linear-gradient(to right, #27272a, #262626)',
      border: '1px solid #52525b',
      borderRadius: '1rem',
      padding: '1.5rem',
      marginBottom: '1.5rem',
      transition: 'all 0.3s',
      flexWrap: 'wrap'
    },
    postLeft: {
      flex: '1 1 400px',
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
      justifyContent: 'space-between'
    },
    postMeta: {
      display: 'flex',
      gap: '1rem',
      fontSize: '0.875rem',
      color: '#9ca3af',
      fontFamily: 'Orbitron, monospace'
    },
    postContent: {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '1rem',
      lineHeight: '1.6',
      color: '#e5e7eb',
      overflow: 'hidden',
      display: '-webkit-box',
      WebkitLineClamp: 4,
      WebkitBoxOrient: 'vertical',
      textOverflow: 'ellipsis'
    },
    postActions: {
      display: 'flex',
      gap: '2rem',
      marginTop: 'auto',
      paddingTop: '1rem',
      borderTop: '1px solid #3f3f46'
    },
    actionButton: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      background: 'transparent',
      border: 'none',
      color: '#9ca3af',
      cursor: 'pointer',
      fontSize: '0.875rem',
      fontFamily: 'Orbitron, monospace',
      padding: '0.5rem',
      transition: 'color 0.2s',
      outline: 'none'
    },
    postRight: {
      flex: '0 1 300px',
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem'
    },
    tickersTitle: {
      fontFamily: 'Orbitron, monospace',
      fontSize: '0.75rem',
      color: '#9ca3af',
      letterSpacing: '0.1em',
      textTransform: 'uppercase',
      marginBottom: '0.5rem'
    },
    tickerBox: {
      background: '#1c1c1e',
      border: '1px solid #3f3f46',
      borderRadius: '0.5rem',
      padding: '1rem'
    },
    ticker: {
      fontFamily: 'Orbitron, monospace',
      fontSize: '1.25rem',
      fontWeight: 'bold',
      color: '#e5e7eb',
      marginBottom: '0.75rem'
    },
    percentRow: {
      display: 'flex',
      justifyContent: 'space-between',
      marginBottom: '0.5rem',
      fontSize: '0.875rem',
      fontFamily: 'Orbitron, monospace'
    },
    percentLabel: {
      color: '#9ca3af'
    },
    loading: {
      textAlign: 'center',
      fontFamily: 'Orbitron, monospace',
      fontSize: '1.5rem',
      marginTop: '5rem',
      color: '#9ca3af'
    }
  };

  if (loading) {
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
        <button 
          style={styles.backButton} 
          onClick={() => window.location.href = '/'}
          onMouseEnter={(e) => e.target.style.background = '#3f3f46'}
          onMouseLeave={(e) => e.target.style.background = 'transparent'}
        >
          <ArrowLeft size={20} />
          Back to Search
        </button>
        <div style={styles.loading}>Loading...</div>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Raleway:wght@200;300&display=swap" rel="stylesheet" />
      </div>
      </>
    );
  }

  if (!data) {
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
        <button 
          style={styles.backButton} 
          onClick={() => window.location.href = '/'}
          onMouseEnter={(e) => e.target.style.background = '#3f3f46'}
          onMouseLeave={(e) => e.target.style.background = 'transparent'}
        >
          <ArrowLeft size={20} />
          Back to Search
        </button>
        <div style={styles.loading}>No data available</div>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Raleway:wght@200;300&display=swap" rel="stylesheet" />
      </div>
      </>
    );
  }

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
        select option {
          background: #27272a;
          color: #e5e7eb;
          padding: 0.5rem;
          border-radius: 0.5rem;
        }
        select:focus option:checked {
          background: #3f3f46;
        }
      `}</style>
      
      <div style={styles.container}>
      <button 
        style={styles.backButton} 
        onClick={() => window.location.href = '/'}
        onMouseEnter={(e) => e.target.style.background = '#3f3f46'}
        onMouseLeave={(e) => e.target.style.background = 'transparent'}
      >
        <ArrowLeft size={20} />
        Back to Search
      </button>

      <div style={styles.header}>
        <h1 style={styles.name}>{displayName}</h1>
        
        <div style={styles.scoresContainer}>
          <div style={styles.scoreBox}>
            <div style={styles.scoreLabel}>One Day Influence Score</div>
            <div style={styles.scoreValue}>
              {data.one_day_influence_score.toFixed(2)}
            </div>
          </div>
          
          <div style={styles.scoreBox}>
            <div style={styles.scoreLabel}>Seven Day Influence Score</div>
            <div style={styles.scoreValue}>
              {data.seven_day_influence_score.toFixed(2)}
            </div>
          </div>
        </div>
      </div>

      <div style={styles.postsContainer}>
        <div style={styles.sortContainer}>
          <span style={styles.sortLabel}>Sort by:</span>
          <div style={styles.customSelect} ref={dropdownRef}>
            <button
              style={styles.selectButton}
              onClick={() => setDropdownOpen(!dropdownOpen)}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#71717a';
                e.currentTarget.style.boxShadow = '0 0 20px rgba(113, 113, 122, 0.3)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = '#52525b';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <span>{sortOptions.find(opt => opt.value === sortBy)?.label}</span>
              <ChevronDown 
                size={20} 
                style={{ 
                  transition: 'transform 0.3s',
                  transform: dropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)'
                }} 
              />
            </button>
            
            {dropdownOpen && (
              <div style={styles.dropdownMenu}>
                {sortOptions.map((option) => (
                  <div
                    key={option.value}
                    style={{
                      ...styles.dropdownOption,
                      background: sortBy === option.value ? '#3f3f46' : 'transparent'
                    }}
                    onClick={() => handleSortChange(option.value)}
                    onMouseEnter={(e) => e.target.style.background = '#3f3f46'}
                    onMouseLeave={(e) => e.target.style.background = sortBy === option.value ? '#3f3f46' : 'transparent'}
                  >
                    {option.label}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {getSortedPosts().map((post) => (
          <div 
            key={post.post_id} 
            style={styles.post}
            onMouseEnter={(e) => e.currentTarget.style.borderColor = '#71717a'}
            onMouseLeave={(e) => e.currentTarget.style.borderColor = '#52525b'}
          >
            {/* Left side - Content and actions */}
            <div style={styles.postLeft}>
              <div>
                <div style={styles.postMeta}>
                  <span>@{post.username}</span>
                  <span>•</span>
                  <span>{new Date(post.timestamp).toLocaleDateString()}</span>
                </div>
                
                <div style={styles.postContent}>
                  {post.content}
                </div>
              </div>

              <div style={styles.postActions}>
                <button
                  style={{
                    ...styles.actionButton,
                    color: likedPosts.has(post.post_id) ? '#ef4444' : '#9ca3af'
                  }}
                  onClick={() => toggleLike(post.post_id)}
                  onMouseEnter={(e) => e.target.style.color = '#ef4444'}
                  onMouseLeave={(e) => e.target.style.color = likedPosts.has(post.post_id) ? '#ef4444' : '#9ca3af'}
                >
                  <Heart 
                    size={20} 
                    fill={likedPosts.has(post.post_id) ? '#ef4444' : 'none'} 
                  />
                  Like
                </button>

                <button
                  style={{
                    ...styles.actionButton,
                    color: repostedPosts.has(post.post_id) ? '#10b981' : '#9ca3af'
                  }}
                  onClick={() => toggleRepost(post.post_id)}
                  onMouseEnter={(e) => e.target.style.color = '#10b981'}
                  onMouseLeave={(e) => e.target.style.color = repostedPosts.has(post.post_id) ? '#10b981' : '#9ca3af'}
                >
                  <Repeat2 size={20} />
                  Repost
                </button>
              </div>
            </div>

            {/* Right side - Tickers */}
            <div style={styles.postRight}>
              <div style={styles.tickersTitle}>Associated Tickers</div>
              {post.price_changes.map((priceChange) => (
                <div key={priceChange.ticker} style={styles.tickerBox}>
                  <div style={styles.ticker}>${priceChange.ticker}</div>
                  
                  <div style={styles.percentRow}>
                    <span style={styles.percentLabel}>1 Day:</span>
                    <span style={{ color: getPercentColor(priceChange.one_day_percent) }}>
                      {formatPercent(priceChange.one_day_percent)}
                    </span>
                  </div>
                  
                  <div style={styles.percentRow}>
                    <span style={styles.percentLabel}>7 Day:</span>
                    <span style={{ color: getPercentColor(priceChange.seven_day_percent) }}>
                      {formatPercent(priceChange.seven_day_percent)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Raleway:wght@200;300&display=swap" rel="stylesheet" />
    </div>
    </>
  );
}