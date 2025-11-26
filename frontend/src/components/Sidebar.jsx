import { useState, useEffect } from 'react';
import Logo from './Logo';
import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  onCopyConversation,
}) {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
  const [showCopyDialog, setShowCopyDialog] = useState(null);

  const handleDeleteClick = (e, convId) => {
    e.stopPropagation();
    setShowDeleteConfirm(convId);
  };

  const handleCopyClick = (e, conv) => {
    e.stopPropagation();
    setShowCopyDialog(conv);
  };

  const confirmDelete = async (convId) => {
    try {
      await onDeleteConversation(convId);
      setShowDeleteConfirm(null);
      // 如果删除的是当前对话，清空选择
      if (convId === currentConversationId) {
        onSelectConversation(null);
      }
    } catch (error) {
      console.error('删除对话失败:', error);
    }
  };

  const confirmCopy = async (conv) => {
    try {
      const newConv = await onCopyConversation(conv.id);
      setShowCopyDialog(null);
      // 选择新复制的对话
      onSelectConversation(newConv.id);
    } catch (error) {
      console.error('复制对话失败:', error);
    }
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <Logo />
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + 新对话
        </button>
      </div>

      <div className="conversation-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">暂无对话记录</div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`conversation-item ${
                conv.id === currentConversationId ? 'active' : ''
              }`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <div className="conversation-content">
                <div className="conversation-title">
                  {conv.title || '新对话'}
                </div>
                <div className="conversation-meta">
                  {conv.message_count} 条消息
                </div>
              </div>
              <div className="conversation-actions">
                <button
                  className="action-btn copy-btn"
                  onClick={(e) => handleCopyClick(e, conv)}
                  title="复制对话"
                >
                  📋
                </button>
                <button
                  className="action-btn delete-btn"
                  onClick={(e) => handleDeleteClick(e, conv.id)}
                  title="删除对话"
                >
                  🗑️
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* 删除确认对话框 */}
      {showDeleteConfirm && (
        <div className="modal-overlay" onClick={() => setShowDeleteConfirm(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>确认删除对话</h3>
            <p>确定要删除这个对话吗？此操作无法撤销。</p>
            <div className="modal-actions">
              <button
                className="btn btn-cancel"
                onClick={() => setShowDeleteConfirm(null)}
              >
                取消
              </button>
              <button
                className="btn btn-danger"
                onClick={() => confirmDelete(showDeleteConfirm)}
              >
                删除
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 复制对话框 */}
      {showCopyDialog && (
        <div className="modal-overlay" onClick={() => setShowCopyDialog(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>复制对话</h3>
            <p>将创建当前对话的完整副本。</p>
            <div className="modal-actions">
              <button
                className="btn btn-cancel"
                onClick={() => setShowCopyDialog(null)}
              >
                取消
              </button>
              <button
                className="btn btn-primary"
                onClick={() => confirmCopy(showCopyDialog)}
              >
                复制
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
